# 💼 Reimbursement Management System

### Odoo x VIT Pune Hackathon Submission

---

## 🚀 Overview

This project is a **role-based expense reimbursement system** designed to streamline how companies manage employee expenses and approval workflows.

It supports:

* Multi-role access (Admin, Manager, Employee)
* Expense submission and tracking
* Approval workflows with intelligent logic
* Company-based data isolation

---

## 👥 Team

* Tejas Joshi — Backend APIs & Core Logic
* Ayush Jadhav — Database & System Layer
* Tanvi Nirbhavane — UI Design
* Tejas Jadhav— API Integration

---

## 🧠 Key Features

### 🔐 Authentication & Company Setup

* On signup:

  * A **new company** is created
  * The first user becomes **Admin**
  * Company currency is set based on country
* Secure login using sessions

---

### 👤 Role-Based Access

#### 🧑‍💼 Admin

* Create employees and managers
* Assign roles
* View all expenses
* Override approvals

#### 🧑‍💻 Manager

* View team expenses
* Approve / Reject with comments

#### 👨‍💼 Employee

* Submit expenses
* View personal expense history

---

### 💸 Expense Submission

Employees can submit:

* Amount (supports multiple currencies)
* Category (Food, Travel, etc.)
* Description
* Date
* Receipt upload (optional)

---

### 🔄 Approval Workflow (Intelligent Feature)

The system implements a **dynamic approval rule**:

* If expense ≤ ₹5000 → Manager approval
* If expense > ₹5000 → Admin approval required

This demonstrates a scalable approval system that can be extended to:

* Multi-level approvals
* Conditional rules (e.g., CFO override, % approval)

---

### 🌍 Currency Conversion

* Real-time currency conversion using API
* Fallback rates ensure reliability even without internet

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript
* **Version Control:** Git + GitHub

---

## 📁 Project Structure

```
backend/
│
├── routes/          # API routes
├── helpers/         # Utility functions (currency conversion)
├── static/          # CSS, JS, uploads
├── templates/       # HTML pages
│
├── app.py           # Main Flask app
├── db.py            # DB connection
├── schema.sql       # Database schema
├── seed.py          # Initial data
```

---

## ⚙️ Setup & Run Instructions

### 1. Clone the repository

```
git clone <your-repo-link>
cd backend
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Initialize database

```
python db.py
python seed.py
```

### 4. Run the server

```
python app.py
```

### 5. Open in browser

```
http://127.0.0.1:5000/login
```

---

## 🔑 Default Admin Login

```
Email: admin@test.com
Password: admin123
```

---

## 🎯 Demo Flow

1. Signup → creates company + admin
2. Login as Admin
3. Create users (Manager / Employee)
4. Login as Employee → submit expense
5. Login as Manager → approve/reject
6. If amount > 5000 → Admin approval required

---

## ⚡ Future Improvements

* Multi-level approval chains
* Percentage-based approval rules
* Real-time notifications
* Advanced analytics dashboard

---

## 🧠 Key Takeaway

This project focuses on:

* Clean architecture
* Working prototype under time constraints
* Scalable logic design

---

## 📌 Note

The system is designed as a **hackathon-ready MVP**, prioritizing functionality and clarity over complexity.

---
