import os
from flask import Flask
from routes.expenses import expenses_bp
from routes.auth import auth_bp # We pre-register this for Tejas

app = Flask(__name__)

# 🔑 ADDED THIS: Necessary for session management (Login/Logout)
app.secret_key = 'supersecretkey' 

# File upload configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Register Blueprints
app.register_blueprint(expenses_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    print("🚀 Backend is live at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)