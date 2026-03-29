from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection
import sqlite3

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# 1. LOGIN ROUTE (The one causing the issue)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    print(f"🔍 Login Attempt: {email}") # Terminal Debugging

    conn = get_db_connection()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()
    finally:
        conn.close()

    if not user:
        print("❌ User not found in database")
        return jsonify({"error": "Invalid credentials"}), 401

    # Check if the hashed password matches
    if not check_password_hash(user['password'], password):
        print("❌ Password hash mismatch")
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ SUCCESS: Set all session variables needed for the UI
    session.clear() # Clear any old/broken sessions
    session['user_id'] = user['id']
    session['role'] = user['role']
    session['company_id'] = user['company_id']
    session['user_name'] = user['name']

    print(f"✅ Login Successful: {user['name']} (Role: {user['role']})")

    return jsonify({
        "message": "Login successful",
        "role": user['role'],
        "name": user['name']
    }), 200

# 2. REGISTER ROUTE (For creating new Companies/Admins)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    name = data.get('name')
    email = data.get('email', '').strip().lower()
    password = data.get('password')
    company_name = data.get('company_name')
    country = data.get('country')
    currency = data.get('currency_code', 'INR')

    if not all([name, email, password, company_name]):
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = generate_password_hash(password)
    
    conn = get_db_connection()
    try:
        # 1. Create the Company
        cursor = conn.execute(
            "INSERT INTO companies (name, country, base_currency) VALUES (?, ?, ?)",
            (company_name, country, currency)
        )
        company_id = cursor.lastrowid

        # 2. Create the Admin User for that company
        conn.execute(
            "INSERT INTO users (company_id, name, email, password, role) VALUES (?, ?, ?, ?, ?)",
            (company_id, name, email, hashed_password, 'Admin')
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered"}), 400
    finally:
        conn.close()

    return jsonify({"message": "Company and Admin registered successfully"}), 201

# 3. LOGOUT ROUTE
@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200