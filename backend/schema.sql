-- 1. Companies Table
-- Stores the high-level organization details and their preferred currency
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT,
    base_currency TEXT NOT NULL
);

-- 2. Users Table
-- Linked to a company. Passwords MUST be stored as hashes (handled in seed.py/auth.py)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'Employee', -- Can be 'Admin', 'Manager', or 'Employee'
    FOREIGN KEY (company_id) REFERENCES companies (id)
);

-- 3. Expenses Table
-- Every expense is tagged with a company_id to prevent data leakage between companies
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    converted_amount REAL NOT NULL, -- The amount in the Company's base_currency
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    status TEXT DEFAULT 'Pending', -- 'Pending', 'Approved', 'Rejected'
    receipt_path TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (company_id) REFERENCES companies (id)
);