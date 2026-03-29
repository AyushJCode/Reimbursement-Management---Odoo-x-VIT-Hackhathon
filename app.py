from flask import Flask
from routes.expenses import expenses_bp
from db import init_db

app = Flask(__name__)

# Initialize the database tables
init_db()

# Register YOUR blueprint
app.register_blueprint(expenses_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)