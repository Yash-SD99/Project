from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = "secret123"  # Needed for session

# Home / Login page
@app.route('/')
def home():
    return render_template('login.html')

# Handle login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Demo credentials
    if email == "admin@poms.com" and password == "admin123":
        session['role'] = 'admin'
        return redirect('/admin')
    elif email == "employee@poms.com" and password == "emp123":
        session['role'] = 'employee'
        return redirect('/employee')
    else:
        flash("Invalid credentials!")
        return redirect('/')

# Admin dashboard
@app.route('/admin')
def admin_dashboard():
    if session.get('role') == 'admin':
        return render_template('admin_dashboard.html')
    flash("Unauthorized access")
    return redirect('/')

# Employee dashboard
@app.route('/employee')
def employee_dashboard():
    if session.get('role') == 'employee':
        return render_template('employee_dashboard.html')
    flash("Unauthorized access")
    return redirect('/')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
