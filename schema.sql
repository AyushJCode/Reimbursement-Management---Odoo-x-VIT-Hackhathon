-- Create Companies Table
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    base_currency TEXT NOT NULL DEFAULT 'INR'
);

-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('Admin', 'Manager', 'Employee')) NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (manager_id) REFERENCES users(id)
);

-- Create Expenses Table
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    converted_amount REAL, -- This will store the INR value for managers
    category TEXT,
    description TEXT,
    date TEXT NOT NULL,
    status TEXT DEFAULT 'Pending', -- Pending, Approved, Rejected
    receipt_path TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);