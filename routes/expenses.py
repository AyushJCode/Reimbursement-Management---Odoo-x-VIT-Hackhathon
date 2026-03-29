from flask import Blueprint, request, jsonify
from db import get_db_connection
from helpers.currency import convert_currency

expenses_bp = Blueprint('expenses', __name__)

@expenses_bp.route('/add-expense', methods=['POST'])
def add_expense():
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
    currency = data.get('currency')
    category = data.get('category')
    date = data.get('date')
    
    # 1. Fetch company base currency for this user (Mocked for now)
    base_currency = 'INR' 
    
    # 2. Convert amount
    converted_amount = convert_currency(amount, currency, base_currency)
    
    # 3. Save to SQLite
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO expenses (user_id, amount, currency, converted_amount, category, date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, amount, currency, converted_amount, category, date, 'Pending'))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Expense submitted successfully!", "converted": converted_amount}), 201