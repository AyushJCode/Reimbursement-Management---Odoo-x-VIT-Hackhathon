from flask import Flask
from routes.expenses import expenses_bp
import os

app = Flask(__name__)

# This tells Flask where to find your uploaded images
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Register your blueprint
app.register_blueprint(expenses_bp)

if __name__ == "__main__":
    # Ensure the upload directory exists before starting
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
        
    app.run(debug=True, port=5000)