import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from db import get_db_connection
from helpers.currency import convert_currency

expenses_bp = Blueprint('expenses', __name__)

# Configuration for file uploads
# Flask will look for this folder relative to where app.py is running
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 1. SUBMIT AN EXPENSE (Employee)
@expenses_bp.route('/add-expense', methods=['POST'])
def add_expense():
    # Use request.form for text and request.files for the image
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
        # Ensure directory exists (app.py usually handles this, but safe to keep)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

    # Convert amount to Company Base Currency (Hardcoded to INR for now)
    base_currency = 'INR' 
    converted_amount = convert_currency(amount, currency, base_currency)
    
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

# 2. GET PERSONAL HISTORY (Employee)
@expenses_bp.route('/get-history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200

# 3. GET ALL EXPENSES (Admin/Manager)
@expenses_bp.route('/admin/all-expenses', methods=['GET'])
def get_all_expenses():
    conn = get_db_connection()
    # Join with users table to show the employee's name to the admin
    query = '''
        SELECT e.*, u.name as employee_name 
        FROM expenses e
        JOIN users u ON e.user_id = u.id
        ORDER BY e.date DESC
    '''
    rows = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200

# 4. APPROVE OR REJECT (Admin/Manager)
@expenses_bp.route('/approve-expense/<int:expense_id>', methods=['POST'])
def approve_expense(expense_id):
    data = request.json
    status = data.get('status') # Expecting "Approved" or "Rejected"
    
    if status not in ['Approved', 'Rejected']:
        return jsonify({"error": "Invalid status code"}), 400

    conn = get_db_connection()
    conn.execute('UPDATE expenses SET status = ? WHERE id = ?', (status, expense_id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"Expense {expense_id} status updated to {status}"}), 200