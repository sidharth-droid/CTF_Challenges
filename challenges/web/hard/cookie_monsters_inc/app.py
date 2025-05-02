from flask import Flask, request, render_template, redirect, url_for, make_response, session
import html
import re
import os
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Flag
FLAG = "FLAG{c00k13_m0nst3r_g0t_th3_cr0mb5}"

# In-memory feedback storage
feedback_entries = []

# Admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = os.environ.get("ADMIN_PASSWORD", "super_secure_password")

# Simple "security" measures
def sanitize_input(text):
    # Remove script tags, but not perfectly...
    text = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', text, flags=re.IGNORECASE)
    # Allow some basic HTML
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    feedback = request.form.get('feedback', '')
    product = request.form.get('product', '')
    
    # "Sanitize" inputs
    name = sanitize_input(name)
    feedback = sanitize_input(feedback)
    
    # Add timestamp
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Save feedback
    feedback_entries.append({
        'name': name,
        'email': email,
        'feedback': feedback,
        'product': product,
        'timestamp': timestamp,
        'reviewed': False
    })
    
    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/feedback')
def view_feedback():
    return render_template('feedback.html', entries=feedback_entries)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            response = redirect(url_for('admin_dashboard'))
            response.set_cookie('admin_session', 'admin_authenticated', httponly=False)
            return response
        else:
            error = 'Invalid credentials'
    
    return render_template('admin_login.html', error=error)

@app.route('/admin/dashboard')
def admin_dashboard():
    # Check for admin cookie as "second factor"
    admin_cookie = request.cookies.get('admin_session')
    print(admin_cookie)
    # If admin cookie is present, allow access regardless of session
    if admin_cookie == 'admin_authenticated':
        return render_template('admin_dashboard.html', flag=FLAG, entries=feedback_entries)
    
    # Otherwise, require session authentication
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    return render_template('admin_dashboard.html', flag=FLAG, entries=feedback_entries)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    response = redirect(url_for('index'))
    response.set_cookie('admin_session', '', expires=0)
    return response

if __name__ == '__main__':
    # Add a default admin feedback entry
    feedback_entries.append({
        'name': 'Admin',
        'email': 'admin@techcorp.com',
        'feedback': 'Testing the feedback system. Everything looks good!',
        'product': 'Security Suite',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'reviewed': True
    })
    
    # app.run(host='0.0.0.0', port=8003, debug=False)