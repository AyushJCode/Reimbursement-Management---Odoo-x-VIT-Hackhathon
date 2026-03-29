from flask import Blueprint, request, jsonify
from db import get_db_connection

approval_bp = Blueprint('approval', __name__)

@approval_bp.route('/pending', methods=['GET'])
def get_pending_approvals():
    conn = get_db_connection()
    
    expenses = conn.execute(
        "SELECT * FROM expenses WHERE status = 'Pending'"
    ).fetchall()
    
    conn.close()

    return jsonify([dict(exp) for exp in expenses])

@approval_bp.route('/action', methods=['POST'])
def approval_action():
    data = request.json

    expense_id = data.get('expense_id')
    action = data.get('action')  # "approve" or "reject"

    if action not in ["approve", "reject"]:
        return jsonify({"error": "Invalid action"}), 400

    new_status = "Approved" if action == "approve" else "Rejected"

    conn = get_db_connection()
    
    conn.execute(
        "UPDATE expenses SET status=? WHERE id=?",
        (new_status, expense_id)
    )
    
    conn.commit()
    conn.close()

    return jsonify({
        "message": f"Expense {new_status}"
    })