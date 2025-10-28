from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))  # 'admin' or 'employee'
    # backref for orders created by this user
    orders = db.relationship('Order', backref='employee', lazy=True)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    # backref for orders for this supplier
    orders = db.relationship('Order', backref='supplier', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # New purchase-order fields
    code = db.Column(db.String(20), unique=True, nullable=False)     # e.g., "PO-001"
    date = db.Column(db.Date, default=date.today, nullable=False)
    amount = db.Column(db.Float, default=0.0)                         # total dollar amount

    # Existing/basic fields (optional to keep)
    product_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

    # Status + relations
    status = db.Column(db.String(20), default="Pending")              # Pending, Approved, Rejected
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id')) # nullable if supplier optional

    def __repr__(self):
        return f"<Order {self.code} {self.status}>"
