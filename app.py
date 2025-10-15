from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = "secret123"  # Needed for session

# -------------------- LOGIN --------------------
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Demo credentials
    if email == "admin@poms.com" and password == "admin123":
        session['role'] = 'admin'
        return redirect('/admin/dashboard')
    elif email == "employee@poms.com" and password == "emp123":
        session['role'] = 'employee'
        return redirect('/employee/dashboard')
    else:
        flash("Invalid credentials! Please try again.")
        return redirect('/')


# -------------------- ADMIN ROUTES --------------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') == 'admin':
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
        return render_template('admin/suppliers.html')
    flash("Unauthorized access")
    return redirect('/')

@app.route('/admin/employees')
def admin_employee():
    if session.get('role') == 'admin':
        return render_template('admin/employees.html')
    flash("Unauthorized access")
    return redirect('/')

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
    app.run(debug=True)
