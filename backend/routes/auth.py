from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    # 1. Define the variables from the request
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    # 2. Hash the password (this creates the 'hashed_password' variable)
    hashed_password = generate_password_hash(password)

    conn = get_db_connection()

    try:
        # 3. Now use them in the query
        conn.execute(
            "INSERT INTO users (name, email, password, role, company_id) VALUES (?, ?, ?, ?, ?)",
            (name, email, hashed_password, "Employee", 1)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": "User already exists or DB error"}), 400

    conn.close()
    return jsonify({"message": "User registered successfully"})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['role'] = user['role']

        return jsonify({
            "message": "Login successful",
            "user_id": user['id'],
            "role": user['role']
        })

    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"})

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    return jsonify({
        "user_id": session['user_id'],
        "role": session['role']
    })


