import os
from flask import Flask, render_template
from routes.auth import auth_bp
from routes.expenses import expenses_bp
from routes.approval_rules import approval_bp

app = Flask(__name__, static_folder='static', template_folder='templates')

# 🔑 CRITICAL: Secret key for Sessions to work
app.secret_key = 'odoo_vit_secret_key_2026'

# 📂 Configure Upload Folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 🔗 Register all Blueprints with their prefixes
app.register_blueprint(auth_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(approval_bp)

# 🌐 Frontend Route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # Ensure upload folder exists so it doesn't crash on first upload
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        
    print("🚀 Project Backend is 100% Integrated!")
    print("📡 Listening at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)