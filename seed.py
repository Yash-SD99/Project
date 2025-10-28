# seed_all.py
from datetime import date
from app import app
from models import db, User, Supplier, Order

def next_code(n):
    return f"PO-{n:03d}"

with app.app_context():
    db.create_all()

    # Users
    if not User.query.first():
        admin = User(name="Admin User", email="admin@poms.com", password="admin123", role="admin")
        emp = User(name="John Employee", email="employee@poms.com", password="emp123", role="employee")
        db.session.add_all([admin, emp])
        db.session.commit()
        print("Users seeded.")
    else:
        admin = User.query.filter_by(role="admin").first()
        emp = User.query.filter_by(role="employee").first()

    # Suppliers
    if not Supplier.query.first():
        sups = [
            Supplier(name="Acme Corp", contact="+1 234-567-8901", email="sales@acme.com", address="123 Business St, NY"),
            Supplier(name="Global Supplies Inc", contact="+1 234-567-8902", email="hello@global.com", address="456 Commerce Ave, CA"),
            Supplier(name="Premier Distributors", contact="+1 234-567-8903", email="contact@premier.com", address="789 Trade Blvd, TX"),
            Supplier(name="Tech Solutions Ltd", contact="+1 234-567-8904", email="info@techsolutions.com", address="321 Innovation Dr, WA"),
        ]
        db.session.add_all(sups)
        db.session.commit()
        print("Suppliers seeded.")

    # Refresh references
    emp = User.query.filter_by(role="employee").first()
    acme = Supplier.query.filter_by(name="Acme Corp").first()
    glob = Supplier.query.filter_by(name="Global Supplies Inc").first()
    prem = Supplier.query.filter_by(name="Premier Distributors").first()
    tech = Supplier.query.filter_by(name="Tech Solutions Ltd").first()

    # Orders
    if not Order.query.first():
        orders = [
            Order(code=next_code(1), date=date(2025,1,15), amount=1250.00, status="Approved",
                  product_name="Printer Paper", quantity=10, employee_id=emp.id, supplier_id=acme.id),
            Order(code=next_code(2), date=date(2025,1,18), amount=3450.00, status="Pending",
                  product_name="HDMI Cables", quantity=50, employee_id=emp.id, supplier_id=glob.id),
            Order(code=next_code(3), date=date(2025,1,20), amount=890.00, status="Approved",
                  product_name="Staplers", quantity=30, employee_id=emp.id, supplier_id=prem.id),
            Order(code=next_code(4), date=date(2025,1,22), amount=2100.00, status="Rejected",
                  product_name="Monitors", quantity=7, employee_id=emp.id, supplier_id=tech.id),
            Order(code=next_code(5), date=date(2025,1,25), amount=1750.00, status="Pending",
                  product_name="Keyboards", quantity=25, employee_id=emp.id, supplier_id=acme.id),
        ]
        db.session.add_all(orders)
        db.session.commit()
        print("Orders seeded.")
    else:
        print("Orders already exist.")

    print("Seeding complete.")
