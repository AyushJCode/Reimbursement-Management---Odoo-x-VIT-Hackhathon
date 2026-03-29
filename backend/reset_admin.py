from db import get_db_connection
from werkzeug.security import generate_password_hash
import os

def hard_reset():
    db_path = 'expenses.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Old database deleted.")

    # Recreate tables
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    
    # Insert Fresh Data
    hashed_pw = generate_password_hash('admin123')
    
    conn.execute("INSERT INTO companies (id, name, country, base_currency) VALUES (1, 'Odoo VIT', 'India', 'INR')")
    
    conn.execute("""
        INSERT INTO users (company_id, name, email, password, role) 
        VALUES (1, 'Admin User', 'admin@test.com', ?, 'Admin')
    """, (hashed_pw,))
    
    conn.commit()
    conn.close()
    print("✨ DATABASE REBUILT!")
    print("📧 Email: admin@test.com")
    print("🔑 Password: admin123")

if __name__ == "__main__":
    hard_reset()