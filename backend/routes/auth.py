from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
import sqlite3

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # ✅ Prevent crash if empty request
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    name = data.get('name')
    email = data.get('email', '').strip().lower()
    password = data.get('password')
    company_name = data.get('company_name')
    country = data.get('country')
    currency_code = data.get('currency_code')

    # ✅ Required fields check
    if not all([name, email, password, company_name, country, currency_code]):
        return jsonify({"error": "All fields required"}), 400

    # ✅ Email validation
    if "@" not in email or "." not in email:
        return jsonify({"error": "Invalid email format"}), 400

    # ✅ Password validation
    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    try:
        # ✅ Step 1: Create company
        cursor = conn.execute(
            "INSERT INTO companies (name, country, base_currency) VALUES (?, ?, ?)",
            (company_name, country, currency_code)
        )
        company_id = cursor.lastrowid

        # ✅ Step 2: First user = Admin
        cursor = conn.execute(
            """INSERT INTO users (name, email, password, role, company_id)
               VALUES (?, ?, ?, 'Admin', ?)""",
            (name, email, hashed_password, company_id)
        )
        user_id = cursor.lastrowid

        conn.commit()

        # ✅ Step 3: Auto-login
        session['user_id'] = user_id
        session['role'] = 'Admin'
        session['company_id'] = company_id

        return jsonify({
            "message": "Company and Admin account created successfully",
            "user_id": user_id,
            "role": "Admin",
            "company_id": company_id
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered"}), 400

    finally:
        conn.close()


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # ✅ Prevent crash
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()
    finally:
        conn.close()

    # ✅ Secure check (no info leak)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ Store session
    session['user_id'] = user['id']
    session['role'] = user['role']
    session['company_id'] = user['company_id']

    return jsonify({
        "message": "Login successful",
        "user_id": user['id'],
        "role": user['role'],
        "company_id": user['company_id']
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    return jsonify({
        "user_id": session['user_id'],
        "role": session['role'],
        "company_id": session['company_id']
    }), 200