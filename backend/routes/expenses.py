import os
from flask import Blueprint, request, jsonify, session
from db import get_db_connection

expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

# 1. SUBMIT AN EXPENSE
@expenses_bp.route('/add-expense', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session.get('user_id')
    company_id = session.get('company_id')
    
    amount = float(request.form.get('amount'))
    currency = request.form.get('currency')
    category = request.form.get('category')
    date = request.form.get('date')
    description = request.form.get('description', '')

    # Simple logic: if USD, multiply by 83 for demo purposes
    converted_amount = amount * 83 if currency == 'USD' else amount

    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO expenses (user_id, company_id, amount, currency, converted_amount, category, description, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, company_id, amount, currency, converted_amount, category, description, date))
        conn.commit()
    finally:
        conn.close()
    
    return jsonify({"message": "Expense submitted"}), 201

# 2. GET PERSONAL HISTORY
@expenses_bp.route('/my-history', methods=['GET'])
def get_history():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (session['user_id'],)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200

# 3. GET STATS FOR REPORTS
@expenses_bp.route('/stats', methods=['GET'])
def get_stats():
    if 'company_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db_connection()
    stats = conn.execute('''
        SELECT category, SUM(converted_amount) as total 
        FROM expenses 
        WHERE company_id = ? AND status = 'Approved'
        GROUP BY category
    ''', (session['company_id'],)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in stats]), 200