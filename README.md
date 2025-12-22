# Orderly – Purchase Order Management System

Orderly is a role-based Purchase Order Management System built using Flask (Python).  
It provides separate dashboards for Admin and Employee users to manage purchase orders efficiently.

---

## Features

### Authentication
- Secure login system using Flask sessions
- Role-based access (Admin / Employee)

### Admin Module
- Admin Dashboard
- Manage Purchase Orders
- Manage Suppliers
- Manage Employees
- View Reports

### Employee Module
- Employee Dashboard
- Create Purchase Orders
- View My Orders

---

## Tech Stack

- Frontend: HTML, CSS
- Backend: Python (Flask)
- Database: SQLite
- ORM: SQLAlchemy
- Version Control: Git, GitHub

---

# Project Structure
```
Orderly/
│── app.py
│── models.py
│── instance/
│   └── orderly.db
│── templates/
│   ├── admin/
│   ├── employee/
│   └── login.html
│── static/
│   ├── css/
│   └── images/
│── README.md
```
---

## Demo Credentials

### Admin
Email: admin@poms.com
Password: admin123

### Employee
Email: employee@poms.com
Password: emp123

---

## Installation & Run

```bash
git clone https://github.com/Yash-SD99/Orderly.git
cd Orderly
pip install flask flask-sqlalchemy
python app.py
```
Open in browser:
http://127.0.0.1:5000/

---

# How It Works
1. User logs in using credentials
2. Role is verified from SQLite database
3. Flask session is created
4. User is redirected to role-based dashboard
5. Admin manages system data
6. Employee creates and tracks orders

---

# Database Schema

### 1. Order Table
Stores purchase order details.

- `id` – Unique identifier for the order
- `code` – Order reference code
- `date` – Order creation date
- `amount` – Total order amount
- `product_name` – Name of the product
- `quantity` – Quantity ordered
- `status` – Order status (Pending, Approved, Rejected)
- `employee_id` – Reference to the employee who created the order
- `supplier_id` – Reference to the supplier

---

### 2. Supplier Table
Stores supplier information.

- `id` – Unique identifier for the supplier
- `name` – Company name of the supplier
- `contact` – Contact number
- `email` – Email address
- `address` – Supplier address

---

### 3. User Table
Stores system user details.

- `id` – Unique identifier for the user
- `name` – Full name of the user
- `email` – Login email
- `password` – Encrypted password
- `role` – User role (`admin` or `employee`)

---

# Future Scope
- Password encryption
- Email notifications
- Cloud deployment

---

# Author
**Yash Deshmukh** <br>
*Computer Engineering Student*
