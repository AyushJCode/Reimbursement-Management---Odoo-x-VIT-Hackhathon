import os
from flask import Flask
from routes.expenses import expenses_bp
from routes.auth import auth_bp  # Pre-importing his work

app = Flask(__name__)

# REQUIRED for Tejas to use Flask Sessions (Login/Logout)
app.secret_key = 'odoo-vit-hackathon-2026-key'

# Upload settings
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Register both parts of the app
app.register_blueprint(expenses_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    print("🚀 Backend is live at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)