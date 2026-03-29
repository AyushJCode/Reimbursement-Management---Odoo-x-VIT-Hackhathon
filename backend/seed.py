from db import get_db_connection

def seed_data():
    conn = get_db_connection()
    
    # 1. Create a Test Company
    conn.execute("""
        INSERT OR IGNORE INTO companies (id, name, base_currency) 
        VALUES (1, 'Odoo VIT Hackathon', 'INR')
    """)
    
    # 2. Create a Test User (Admin/Manager)
    # We use ID 1 so you can easily reference it in Postman
    conn.execute("""
        INSERT OR IGNORE INTO users (id, company_id, name, email, password, role) 
        VALUES (1, 1, 'Ayush Admin', 'admin@test.com', 'admin123', 'Admin')
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database Seeded!")
    print("👉 Test User ID: 1")
    print("👉 Test Company ID: 1")

if __name__ == "__main__":
    seed_data()