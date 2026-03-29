from db import get_db_connection
from werkzeug.security import generate_password_hash

def seed_data():
    conn = get_db_connection()
    hashed_pw = generate_password_hash('admin123') 
    
    # 1. Seed Company first
    conn.execute("""
        INSERT OR IGNORE INTO companies (id, name, country, base_currency) 
        VALUES (1, 'Odoo VIT Hackathon', 'India', 'INR')
    """)
    
    # 2. Seed Admin with the company_id
    conn.execute("""
        INSERT OR IGNORE INTO users (id, company_id, name, email, password, role) 
        VALUES (1, 1, 'Ayush Admin', 'admin@test.com', ?, 'Admin')
    """, (hashed_pw,))
    
    conn.commit()
    conn.close()
    print("✅ Database Seeded with New Schema!")

if __name__ == "__main__":
    seed_data()