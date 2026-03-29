# Odoo Reimbursement Management System
**VIT Hackathon 2026**

A multi-tenant expense management solution designed to automate manual reimbursement processes, eliminate errors, and provide full spending transparency.

## 👥 The Team
* [cite_start]**Tejas Joshi (Leader)** — Backend APIs & Core Logic [cite: 52]
* [cite_start]**Ayush Jadhav** — Database & System Layer [cite: 9, 11]
* [cite_start]**Tanvi Nirbhvane** — UI Design [cite: 56]
* [cite_start]**Tejas Jadhav** — API Integration [cite: 55]

## 🚀 Key Features
* [cite_start]**Multi-Tenant Isolation**: Uses a `company_id` architecture to ensure that data for one company is never visible to another, satisfying strict data privacy. [cite: 48]
* [cite_start]**Automated Currency Engine**: Supports global expense claims in various currencies (e.g., USD) with automatic conversion to the company’s base currency (INR) for manager review. [cite: 19, 50, 55]
* **Role-Based Access Control (RBAC)**: 
    * [cite_start]**Admin**: Manage users, configure rules, and view all company expenses. [cite: 12, 48]
    * [cite_start]**Manager**: Review team expenses and approve/reject pending claims. [cite: 35, 49, 50]
    * [cite_start]**Employee**: Submit claims with descriptions and track approval history. [cite: 17, 18, 51]
* [cite_start]**Real-Time Workflow**: Instant synchronization between employee submissions and the manager’s approval queue. [cite: 33]
* [cite_start]**Data Integrity**: Implemented strict validation for business emails and professional naming conventions. [cite: 9, 10]

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
