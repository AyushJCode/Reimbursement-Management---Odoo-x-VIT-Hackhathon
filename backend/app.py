import os
from flask import Flask, render_template
from routes.auth import auth_bp
from routes.expenses import expenses_bp
from routes.approval_rules import approval_bp

app = Flask(__name__, static_folder='static', template_folder='templates')

# 🔑 CRITICAL: This allows Flask to store user_id and company_id in the browser
app.secret_key = 'odoo_vit_secret_key_2026'

# 📂 Configure Upload Folder for Receipts
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 🔗 Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(approval_bp)

# 🌐 Single Page Route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # Auto-create upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        
    print("🚀 Odoo Reimbursement System Active!")
    print("📡 Listening at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)