from flask import Blueprint, request, jsonify, session
from db import get_db_connection

approval_bp = Blueprint('approval', __name__, url_prefix='/approvals')


# 🔹 Get pending approvals (Manager/Admin only)
@approval_bp.route('/pending', methods=['GET'])
def get_pending_approvals():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    if session.get('role') not in ["Admin", "Manager"]:
        return jsonify({"error": "Unauthorized"}), 403

    conn = get_db_connection()

    expenses = conn.execute(
        """
        SELECT * FROM expenses
        WHERE status = 'Pending' AND company_id = ?
        """,
        (session['company_id'],)
    ).fetchall()

    conn.close()

    return jsonify([dict(exp) for exp in expenses]), 200


# 🔹 Approve or Reject expense
@approval_bp.route('/action', methods=['POST'])
def approval_action():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401

    role = session.get('role')

    if role not in ["Admin", "Manager"]:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    expense_id = data.get('expense_id')
    action = data.get('action')

    if not expense_id or action not in ["approve", "reject"]:
        return jsonify({"error": "Invalid input"}), 400

    conn = get_db_connection()

    expense = conn.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    ).fetchone()

    if not expense:
        conn.close()
        return jsonify({"error": "Expense not found"}), 404

    # 🔥 Company isolation (VERY IMPORTANT)
    if expense['company_id'] != session['company_id']:
        conn.close()
        return jsonify({"error": "Unauthorized access"}), 403

    # 🔥 Intelligent approval logic
    if expense['converted_amount'] > 5000:
        required_role = "Admin"
    else:
        required_role = "Manager"

    if role != required_role and role != "Admin":
        conn.close()
        return jsonify({
            "error": f"{required_role} approval required for this expense"
        }), 403

    # 🔹 Update status
    new_status = "Approved" if action == "approve" else "Rejected"

    conn.execute(
        "UPDATE expenses SET status = ? WHERE id = ?",
        (new_status, expense_id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": f"Expense {new_status}",
        "approved_by": role
    }), 200