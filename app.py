from flask import Flask, render_template, request, redirect, session, flash, Response, url_for
from sqlalchemy import and_, func
from models import db, User, Supplier, Order  # Order is available for future pages
from datetime import datetime, date

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
    if session.get('role') != 'admin':
        flash("Unauthorized access"); return redirect('/')

    total_orders = Order.query.count()
    approved = Order.query.filter_by(status="Approved").count()
    pending = Order.query.filter_by(status="Pending").count()
    rejected = Order.query.filter_by(status="Rejected").count()
    total_suppliers = Supplier.query.count()
    total_employees = User.query.filter_by(role='employee').count()
    spend_approved = db.session.query(func.coalesce(func.sum(Order.amount), 0.0)).filter(Order.status=="Approved").scalar()

    # latest 5
    latest_orders = Order.query.order_by(Order.id.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           total_orders=total_orders,
                           approved=approved,
                           pending=pending,
                           rejected=rejected,
                           total_suppliers=total_suppliers,
                           total_employees=total_employees,
                           spend_approved=round(spend_approved or 0, 2),
                           latest_orders=latest_orders)


@app.route('/admin/orders')
def admin_orders():
    if session.get('role') == 'admin':
        orders = Order.query.order_by(Order.id).all()
        return render_template('admin/orders.html', orders=orders)
    flash("Unauthorized access"); return redirect('/')

@app.route('/admin/orders/<int:order_id>/status', methods=['POST'])
def admin_orders_status(order_id):
    if session.get('role') != 'admin':
        flash("Unauthorized access"); return redirect('/')
    o = Order.query.get_or_404(order_id)
    o.status = request.form.get('status','Pending')
    db.session.commit()
    flash(f"Order {o.code} set to {o.status}.")
    return redirect('/admin/orders')

@app.route('/admin/orders/<int:order_id>/delete', methods=['POST'])
def admin_orders_delete(order_id):
    if session.get('role') != 'admin':
        flash("Unauthorized access"); return redirect('/')
    o = Order.query.get_or_404(order_id)
    db.session.delete(o)
    db.session.commit()
    flash("Order deleted.")
    return redirect('/admin/orders')


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
    if session.get('role') != 'admin':
        flash("Unauthorized access"); return redirect('/')

    # Filters
    status = request.args.get('status', '').strip()
    supplier_id = request.args.get('supplier_id', '').strip()
    employee_id = request.args.get('employee_id', '').strip()
    date_str = request.args.get('date', '').strip()

    q = Order.query
    conds = []

    if status:
        conds.append(Order.status == status)

    if supplier_id:
        try:
            conds.append(Order.supplier_id == int(supplier_id))
        except ValueError:
            pass

    if employee_id:
        try:
            conds.append(Order.employee_id == int(employee_id))
        except ValueError:
            pass

    # Single date filter (equals match)
    def parse_d(s):
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except Exception:
            return None

    d = parse_d(date_str)
    if d:
        conds.append(Order.date == d)

    if conds:
        q = q.filter(and_(*conds))

    q = q.order_by(Order.date.desc(), Order.id.desc())
    orders = q.all()

    total_amount = sum((o.amount or 0) for o in orders)
    suppliers = Supplier.query.order_by(Supplier.name).all()
    employees = User.query.filter_by(role='employee').order_by(User.name).all()

    return render_template('admin/reports.html',
                           orders=orders,
                           suppliers=suppliers,
                           employees=employees,
                           status=status,
                           supplier_id=supplier_id,
                           employee_id=employee_id,
                           date=date_str,
                           total_amount=round(total_amount, 2))

# View a single order in a new page (no PDF)
@app.route('/admin/orders/<int:order_id>/view')
def admin_order_view(order_id):
    if session.get('role') != 'admin':
        flash("Unauthorized access"); return redirect('/')

    o = Order.query.get_or_404(order_id)
    return render_template('admin/order_view.html', o=o, generated_at=datetime.now())


# -------------------- EMPLOYEE ROUTES --------------------
# Employee dashboard with live counts
@app.route('/employee/dashboard')
def employee_dashboard():
    if session.get('role') != 'employee':
        flash("Unauthorized access"); return redirect('/')
    uid = session.get('user_id')
    total = Order.query.filter_by(employee_id=uid).count()
    pending = Order.query.filter_by(employee_id=uid, status="Pending").count()
    approved = Order.query.filter_by(employee_id=uid, status="Approved").count()
    rejected = Order.query.filter_by(employee_id=uid, status="Rejected").count()
    return render_template('employee/dashboard.html',
                           total=total, pending=pending, approved=approved, rejected=rejected)

# My orders list
@app.route('/employee/myOrders')
def employee_myorders():
    if session.get('role') != 'employee':
        flash("Unauthorized access"); return redirect('/')
    uid = session.get('user_id')
    orders = Order.query.filter_by(employee_id=uid).order_by(Order.id.desc()).all()
    return render_template('employee/myOrders.html', orders=orders)

# Create order page
@app.route('/employee/createOrder')
def employee_createorders():
    if session.get('role') != 'employee':
        flash("Unauthorized access"); return redirect('/')
    suppliers = Supplier.query.order_by(Supplier.name).all()
    return render_template('employee/createOrder.html', suppliers=suppliers)

# Handle order submission
def _next_order_code():
    last = Order.query.order_by(Order.id.desc()).first()
    n = (last.id + 1) if last else 1
    return f"PO-{n:03d}"

@app.route('/employee/createOrder', methods=['POST'])
def employee_createorders_post():
    if session.get('role') != 'employee':
        flash("Unauthorized access"); return redirect('/')

    uid = session.get('user_id')
    supplier_id = request.form.get('supplier_id')
    product_name = request.form.get('product_name','').strip()
    quantity = request.form.get('quantity','0').strip()
    amount = request.form.get('amount','0').strip()
    date_str = request.form.get('date','').strip()

    # Basic validation
    try:
        quantity = int(quantity or 0)
    except ValueError:
        quantity = 0
    try:
        amount = float(amount or 0)
    except ValueError:
        amount = 0.0
    try:
        d = date.fromisoformat(date_str) if date_str else date.today()
    except ValueError:
        d = date.today()

    if not supplier_id or not product_name or quantity <= 0:
        flash("Please fill supplier, product, and a positive quantity.")
        return redirect('/employee/createOrder')

    code = _next_order_code()
    order = Order(code=code,
                  supplier_id=int(supplier_id),
                  employee_id=uid,
                  product_name=product_name,
                  quantity=quantity,
                  amount=amount,
                  date=d,
                  status="Pending")
    db.session.add(order)
    db.session.commit()
    flash(f"Order {code} submitted.")
    return redirect('/employee/myOrders')

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
