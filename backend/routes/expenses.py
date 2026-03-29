import os
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from db import get_db_connection
from helpers.currency import convert_currency

# ✅ Added url_prefix for a professional API structure
expenses_bp = Blueprint('expenses', __name__, url_prefix='/expenses')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 1. SUBMIT AN EXPENSE (Employee)
@expenses_bp.route('/add-expense', methods=['POST'])
def add_expense():
    # 🔥 Security Check: Must be logged in
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized. Please login first."}), 401

    user_id = session.get('user_id')
    company_id = session.get('company_id') # 🛡️ Automatic Company Tagging
    
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
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

    # Convert amount to Company Base Currency
    # In a real app, you'd fetch the company's base_currency from the DB here
    base_currency = 'INR' 
    converted_amount = convert_currency(amount, currency, base_currency)
    
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO expenses (user_id, company_id, amount, currency, converted_amount, category, description, date, status, receipt_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, company_id, amount, currency, converted_amount, category, description, date, 'Pending', filename))
        
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": f"Database Error: {str(e)}"}), 500
        
    conn.close()
    
    return jsonify({
        "message": "Expense submitted successfully!", 
        "converted_amount": f"{base_currency} {converted_amount}",
        "receipt_saved": filename
    }), 201

# 2. GET PERSONAL HISTORY (Employee)
@expenses_bp.route('/my-history', methods=['GET'])
def get_history():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    user_id = session.get('user_id')
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC', (user_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200

# 3. GET ALL COMPANY EXPENSES (Admin/Manager)
@expenses_bp.route('/all', methods=['GET'])
def get_all_expenses():
    if 'user_id' not in session or session.get('role') not in ['Admin', 'Manager']:
        return jsonify({"error": "Unauthorized access"}), 403

    company_id = session.get('company_id')
    conn = get_db_connection()
    
    # 🔥 Join with users to show employee names
    query = '''
        SELECT e.*, u.name as employee_name 
        FROM expenses e
        JOIN users u ON e.user_id = u.id
        WHERE e.company_id = ?
        ORDER BY e.date DESC
    '''
    rows = conn.execute(query, (company_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows]), 200