import sqlite3
import os

DATABASE = 'expenses.db'

def get_db_connection():
    """Creates a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    # This line allows you to access columns by name (e.g., row['email']) 
    # instead of index (e.g., row[1])
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """Initializes the database using the schema.sql file."""
    # We only run this if the .db file doesn't exist yet
    if not os.path.exists(DATABASE):
        print("Creating database...")
        conn = get_db_connection()
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully! 'expenses.db' created.")
    else:
        print("ℹ️ Database already exists. No changes made.")

if __name__ == "__main__":
    init_db()