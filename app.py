# from flask import Flask, render_template, request, redirect, session, flash
# from models import db, User  # import db instance and User model

# app = Flask(__name__)
# app.secret_key = "secret123"  # Needed for session

# # -------------------- SQLite / SQLAlchemy --------------------
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orderly.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db.init_app(app)

# # -------------------- LOGIN --------------------
# @app.route('/')
# def home():
#     return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def login():
#     email = request.form['email'].strip()
#     password = request.form['password'].strip()

#     # Look up user in SQLite
#     user = User.query.filter_by(email=email, password=password).first()
#     if not user:
#         flash("Invalid credentials! Please try again.")
#         return redirect('/')

#     session['role'] = user.role
#     session['user_id'] = user.id
#     session['user_name'] = user.name

#     if user.role == 'admin':
#         return redirect('/admin/dashboard')
#     else:
#         return redirect('/employee/dashboard')

# # -------------------- ADMIN ROUTES --------------------
# @app.route('/admin/dashboard')
# def admin_dashboard():
#     if session.get('role') == 'admin':
#         return render_template('admin/dashboard.html')
#     flash("Unauthorized access")
#     return redirect('/')

# @app.route('/admin/orders')
# def admin_orders():
#     if session.get('role') == 'admin':
#         return render_template('admin/orders.html')
#     flash("Unauthorized access")
#     return redirect('/')

# from models import Supplier

# @app.route('/admin/suppliers')
# def admin_suppliers():
#     if session.get('role') == 'admin':
#         suppliers = Supplier.query.order_by(Supplier.name).all()
#         return render_template('admin/suppliers.html', suppliers=suppliers)
#     flash("Unauthorized access")
#     return redirect('/')


# @app.route('/admin/employees')
# def admin_employee():
#     if session.get('role') == 'admin':
#         return render_template('admin/employees.html')
#     flash("Unauthorized access")
#     return redirect('/')

# @app.route('/admin/reports')
# def admin_reports():
#     if session.get('role') == 'admin':
#         return render_template('admin/reports.html')
#     flash("Unauthorized access")
#     return redirect('/')

# # -------------------- EMPLOYEE ROUTES --------------------
# @app.route('/employee/dashboard')
# def employee_dashboard():
#     if session.get('role') == 'employee':
#         return render_template('employee/dashboard.html')
#     flash("Unauthorized access")
#     return redirect('/')

# @app.route('/employee/myOrders')
# def employee_myorders():
#     if session.get('role') == 'employee':
#         return render_template('employee/myOrders.html')
#     flash("Unauthorized access")
#     return redirect('/')

# @app.route('/employee/createOrder')
# def employee_createorders():
#     if session.get('role') == 'employee':
#         return render_template('employee/createOrder.html')
#     flash("Unauthorized access")
#     return redirect('/')

# # -------------------- LOGOUT --------------------
# @app.route('/logout')
# def logout():
#     session.clear()
#     flash("You have been logged out successfully.")
#     return redirect('/')

# # -------------------- MAIN --------------------
# if __name__ == "__main__":
#     # create tables on first run
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)

# from models import Supplier

# #add suppliers
# @app.route('/admin/suppliers/add', methods=['POST'])
# def admin_suppliers_add():
#     if session.get('role') != 'admin':
#         flash("Unauthorized access")
#         return redirect('/')

#     name = request.form.get('name','').strip()
#     contact = request.form.get('contact','').strip()
#     email = request.form.get('email','').strip()
#     address = request.form.get('address','').strip()

#     if not name:
#         flash("Supplier name is required.")
#         return redirect('/admin/suppliers')

#     s = Supplier(name=name, contact=contact, email=email, address=address)
#     from models import db
#     db.session.add(s)
#     db.session.commit()
#     flash("Supplier added.")
#     return redirect('/admin/suppliers')

from flask import Flask, render_template, request, redirect, session, flash
from models import db, User, Supplier, Order  # Order is available for future pages

app = Flask(__name__)
app.secret_key = "secret123"  # Needed for session

# -------------------- SQLite / SQLAlchemy --------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orderly.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# -------------------- LOGIN --------------------
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email'].strip()
    password = request.form['password'].strip()

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        flash("Invalid credentials! Please try again.")
        return redirect('/')

    session['role'] = user.role
    session['user_id'] = user.id
    session['user_name'] = user.name

    if user.role == 'admin':
        return redirect('/admin/dashboard')
    else:
        return redirect('/employee/dashboard')

# -------------------- ADMIN ROUTES --------------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') == 'admin':
        # You can compute real counts later from Order
        return render_template('admin/dashboard.html')
    flash("Unauthorized access")
    return redirect('/')

@app.route('/admin/orders')
def admin_orders():
    if session.get('role') == 'admin':
        return render_template('admin/orders.html')
    flash("Unauthorized access")
    return redirect('/')

@app.route('/admin/suppliers')
def admin_suppliers():
    if session.get('role') == 'admin':
        suppliers = Supplier.query.order_by(Supplier.name).all()
        return render_template('admin/suppliers.html', suppliers=suppliers)
    flash("Unauthorized access")
    return redirect('/')

# Create supplier (works with the dialog form in suppliers.html)
@app.route('/admin/suppliers/add', methods=['POST'])
def admin_suppliers_add():
    if session.get('role') != 'admin':
        flash("Unauthorized access")
        return redirect('/')

    name = request.form.get('name', '').strip()
    contact = request.form.get('contact', '').strip()
    email = request.form.get('email', '').strip()
    address = request.form.get('address', '').strip()

    if not name:
        flash("Supplier name is required.")
        return redirect('/admin/suppliers')

    s = Supplier(name=name, contact=contact, email=email, address=address)
    db.session.add(s)
    db.session.commit()
    flash("Supplier added.")
    return redirect('/admin/suppliers')

# Edit supplier
@app.route('/admin/suppliers/<int:supplier_id>/edit', methods=['POST'])
def admin_suppliers_edit(supplier_id):
    if session.get('role') != 'admin':
        flash("Unauthorized access")
        return redirect('/')

    s = Supplier.query.get_or_404(supplier_id)

    name = request.form.get('name','').strip()
    contact = request.form.get('contact','').strip()
    email = request.form.get('email','').strip()
    address = request.form.get('address','').strip()

    if not name:
        flash("Supplier name is required.")
        return redirect('/admin/suppliers')

    s.name = name
    s.contact = contact
    s.email = email
    s.address = address
    db.session.commit()
    flash("Supplier updated.")
    return redirect('/admin/suppliers')

# Delete supplier
@app.route('/admin/suppliers/<int:supplier_id>/delete', methods=['POST'])
def admin_suppliers_delete(supplier_id):
    if session.get('role') != 'admin':
        flash("Unauthorized access")
        return redirect('/')

    s = Supplier.query.get_or_404(supplier_id)
    db.session.delete(s)
    db.session.commit()
    flash("Supplier deleted.")
    return redirect('/admin/suppliers')


@app.route('/admin/employees')
def admin_employee():
    if session.get('role') == 'admin':
        employees = User.query.filter_by(role='employee').order_by(User.id).all()
        return render_template('admin/employees.html', employees=employees)
    flash("Unauthorized access")
    return redirect('/')

@app.route('/admin/employees/add', methods=['POST'])
def admin_employees_add():
    if session.get('role') != 'admin':
        flash("Unauthorized access")
        return redirect('/')

    name = request.form.get('name','').strip()
    email = request.form.get('email','').strip().lower()
    password = request.form.get('password','').strip()
    role = request.form.get('role','employee')

    if not name or not email or not password:
        flash("Name, email and password are required.")
        return redirect('/admin/employees')

    # prevent duplicates
    if User.query.filter_by(email=email).first():
        flash("Email already exists.")
        return redirect('/admin/employees')

    u = User(name=name, email=email, password=password, role=role)
    db.session.add(u)
    db.session.commit()
    flash("Employee added.")
    return redirect('/admin/employees')

# Update employee
@app.route('/admin/employees/<int:user_id>/edit', methods=['POST'])
def admin_employees_edit(user_id):
    if session.get('role') != 'admin':
        flash("Unauthorized access")
        return redirect('/')

    u = User.query.get_or_404(user_id)

    name = request.form.get('name','').strip()
    email = request.form.get('email','').strip().lower()
    role = request.form.get('role','employee')
    password = request.form.get('password','').strip()  # optional

    if not name or not email:
        flash("Name and email are required.")
        return redirect('/admin/employees')

    # unique email except for current user
    exists = User.query.filter(User.email == email, User.id != u.id).first()
    if exists:
        flash("Email already exists.")
        return redirect('/admin/employees')

    u.name = name
    u.email = email
    u.role = role
    if password:
        u.password = password  # for demo; hash later

    db.session.commit()
    flash("Employee updated.")
    return redirect('/admin/employees')

# Delete employee
@app.route('/admin/employees/<int:user_id>/delete', methods=['POST'])
def admin_employees_delete(user_id):
    if session.get('role') != 'admin':
        flash("Unauthorized access")
        return redirect('/')

    u = User.query.get_or_404(user_id)
    if u.id == session.get('user_id'):
        flash("You cannot delete your own account.")
        return redirect('/admin/employees')

    db.session.delete(u)
    db.session.commit()
    flash("Employee deleted.")
    return redirect('/admin/employees')


@app.route('/admin/reports')
def admin_reports():
    if session.get('role') == 'admin':
        return render_template('admin/reports.html')
    flash("Unauthorized access")
    return redirect('/')

# -------------------- EMPLOYEE ROUTES --------------------
@app.route('/employee/dashboard')
def employee_dashboard():
    if session.get('role') == 'employee':
        return render_template('employee/dashboard.html')
    flash("Unauthorized access")
    return redirect('/')

@app.route('/employee/myOrders')
def employee_myorders():
    if session.get('role') == 'employee':
        return render_template('employee/myOrders.html')
    flash("Unauthorized access")
    return redirect('/')

@app.route('/employee/createOrder')
def employee_createorders():
    if session.get('role') == 'employee':
        # If you later want to populate the supplier <select>, pass Supplier.query.all()
        return render_template('employee/createOrder.html')
    flash("Unauthorized access")
    return redirect('/')

# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.")
    return redirect('/')

# -------------------- MAIN --------------------
if __name__ == "__main__":
    # create tables on first run
    with app.app_context():
        db.create_all()
    app.run(debug=True)
