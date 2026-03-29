from flask import Blueprint, request, jsonify
from db import get_db_connection
from helpers.currency import convert_currency

# Define the Blueprint
expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
    currency = data.get('currency')
    category = data.get('category')
    date = data.get('date')
    description = data.get('description', '') # Added description with a default empty string
    
    # 1. Fetch company base currency for this user (Keep mocked for now or fetch from DB)
    base_currency = 'INR' 
    
    # 2. Convert amount
    converted_amount = convert_currency(amount, currency, base_currency)
    
    # 3. Save to SQLite
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO expenses (user_id, amount, currency, converted_amount, category, description, date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, amount, currency, converted_amount, category, description, date, 'Pending'))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "message": "Expense submitted successfully!", 
        "converted": converted_amount
    }), 201

@expenses_bp.route('/get-history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    """
    Fetches all expenses for a specific user to display in the dashboard table.
    """
    conn = get_db_connection()
    # Fetch rows and sort by newest date first
    rows = conn.execute('''
        SELECT id, amount, currency, converted_amount, category, description, date, status 
        FROM expenses 
        WHERE user_id = ? 
        ORDER BY date DESC
    ''', (user_id,)).fetchall()
    conn.close()
    
    # Transform SQLite rows into a list of dictionaries for the Frontend
    history = [dict(row) for row in rows]
    return jsonify(history), 200