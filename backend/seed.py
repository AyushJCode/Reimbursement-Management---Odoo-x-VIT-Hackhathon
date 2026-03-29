from db import get_db_connection
from werkzeug.security import generate_password_hash

def seed_data():
    conn = get_db_connection()
    # 🔑 This is the magic part: it turns 'admin123' into a secure hash
    hashed_pw = generate_password_hash('admin123') 
    
    conn.execute("INSERT OR IGNORE INTO companies (id, name, base_currency) VALUES (1, 'Odoo VIT Hackathon', 'INR')")
    
    # We insert the HASH, not the plain text password
    conn.execute("""
        INSERT OR IGNORE INTO users (id, company_id, name, email, password, role) 
        VALUES (1, 1, 'Ayush Admin', 'admin@test.com', ?, 'Admin')
    """, (hashed_pw,))
    
    conn.commit()
    conn.close()
    print("✅ Database Reset and Seeded with Hashed Password!")

if __name__ == "__main__":
    seed_data()