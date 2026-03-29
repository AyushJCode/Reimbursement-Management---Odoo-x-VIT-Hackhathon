import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from db import get_db_connection
from helpers.currency import convert_currency

expenses_bp = Blueprint('expenses', __name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@expenses_bp.route('/add-expense', methods=['POST'])
def add_expense():
    # Since we are sending a file, we use request.form instead of request.json
    user_id = request.form.get('user_id')
    amount = float(request.form.get('amount'))
    currency = request.form.get('currency')
    category = request.form.get('category')
    date = request.form.get('date')
    description = request.form.get('description', '')

    # Handle File Upload
    file = request.files.get('receipt')
    filename = None
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Create a unique path for the file
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

    # 1. Fetch company base currency (Mocked or DB fetch)
    base_currency = 'INR' 
    
    # 2. Convert amount
    converted_amount = convert_currency(amount, currency, base_currency)
    
    # 3. Save to SQLite (Including the receipt_path)
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO expenses (user_id, amount, currency, converted_amount, category, description, date, status, receipt_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, amount, currency, converted_amount, category, description, date, 'Pending', filename))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "message": "Expense and Receipt submitted successfully!", 
        "receipt_saved": filename
    }), 201