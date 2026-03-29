from db import get_db_connection
from werkzeug.security import generate_password_hash

def seed_data():
    conn = get_db_connection()
    # 🔑 This creates the secure string for 'admin123'
    hashed_pw = generate_password_hash('admin123') 
    
    # Clear old data to be safe
    conn.execute("DELETE FROM users")
    conn.execute("DELETE FROM companies")

    # 1. Seed Company
    conn.execute("""
        INSERT INTO companies (id, name, country, base_currency) 
        VALUES (1, 'Odoo VIT', 'India', 'INR')
    """)
    
    # 2. Seed Admin User (Linked to Company 1)
    conn.execute("""
        INSERT INTO users (company_id, name, email, password, role) 
        VALUES (1, 'Ayush Admin', 'admin@test.com', ?, 'Admin')
    """, (hashed_pw,))
    
    conn.commit()
    conn.close()
    print("✅ SEED SUCCESS: User 'admin@test.com' created with password 'admin123'")

if __name__ == "__main__":
    seed_data()