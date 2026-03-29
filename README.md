# Odoo Reimbursement Management System
**VIT Hackathon 2026**

A multi-tenant expense management solution designed to automate manual reimbursement processes, eliminate errors, and provide full spending transparency.

## 👥 The Team
* **Tejas Joshi (Leader)** — Backend APIs & Core Logic
* **Ayush Jadhav** — Database & System Layer
* **Tanvi Nirbhvane** — UI Design
* **Tejas Jadhav** — API Integration

## 🚀 Key Features
* **Multi-Tenant Isolation**: Uses a `company_id` architecture to ensure that data for one company is never visible to another, satisfying strict data privacy. 
* **Automated Currency Engine**: Supports global expense claims in various currencies (e.g., USD) with automatic conversion to the company’s base currency (INR) for manager review
* **Role-Based Access Control (RBAC)**: 
    * **Admin**: Manage users, configure rules, and view all company expenses. 
    * **Manager**: Review team expenses and approve/reject pending claims.
    * **Employee**: Submit claims with descriptions and track approval history. 
* **Real-Time Workflow**: Instant synchronization between employee submissions and the manager’s approval queue.
* **Data Integrity**: Implemented strict validation for business emails and professional naming conventions.

## 🛠️ Tech Stack
* **Backend**: Python / Flask
* **Database**: SQLite (Relational Schema)
* **Frontend**: HTML5, CSS3 (Odoo-Branded UI), JavaScript (Vanilla ES6)
* **Security**: Password Hashing via Werkzeug

## 📋 Prerequisites
* Python 3.8+
* Browser (Chrome/Edge/Firefox)

## ⚙️ Setup & Installation
Follow these steps to initialize the environment and the database:

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
