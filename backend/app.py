import os
from flask import Flask
from routes.expenses import expenses_bp
from routes.auth import auth_bp
from routes.approval_rules import approval_bp

app = Flask(__name__)

# 🔑 Added 'supersecretkey' as Tejas requested for session management
app.secret_key = "supersecretkey"

# Configuration for file uploads
# This ensures receipts are saved in backend/static/uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# --- Blueprint Registration ---
# 1. Expense Management (Your core logic)
app.register_blueprint(expenses_bp)

# 2. User Authentication (Tejas's Login/Register logic)
app.register_blueprint(auth_bp)

# 3. Manager Approvals (Tejas's new Pending/Action logic)
app.register_blueprint(approval_bp)

if __name__ == "__main__":
    # Ensure the upload directory exists relative to the backend folder
    upload_path = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        print(f"📁 Created upload directory at: {upload_path}")
        
    print("🚀 Project Backend is 100% Integrated!")
    print("📡 Listening at http://127.0.0.1:5000")
    
    app.run(debug=True, port=5000)