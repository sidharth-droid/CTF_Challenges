from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    """Set up the database with users and secrets tables."""
    conn = sqlite3.connect('ctf.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS secrets (flag TEXT)')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'secretpassword')")
    c.execute("INSERT OR IGNORE INTO secrets (flag) VALUES ('FLAG{blind_sql_bandit_win}')")
    conn.commit()
    conn.close()

# HTML template with Bootstrap for a clean UI
LOGIN_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blind SQL Bandit</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f8f9fa;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
        }
        .form-title {
            text-align: center;
            margin-bottom: 1.5rem;
            color: #343a40;
        }
        .message {
            text-align: center;
            margin-top: 1rem;
            color: {{ message_color }};
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2 class="form-title">Login Portal</h2>
        <form method="POST">
            <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input type="text" class="form-control" id="username" name="username" placeholder="Enter username" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" name="password" placeholder="Enter password" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Login</button>
        </form>
        <p class="message">{{ message }}</p>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle login requests and check for SQLi vulnerability."""
    message = ''
    message_color = '#dc3545'  # Default red for errors

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vulnerable SQL query (blind SQLi)
        conn = sqlite3.connect('ctf.db')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        try:
            c.execute(query)
            result = c.fetchone()
            if result:
                message = "Login successful!"
                message_color = '#28a745'  # Green for success
            else:
                message = "Login failed!"
        except sqlite3.Error:
            message = "Something went wrong!"
        finally:
            conn.close()

    return render_template_string(LOGIN_PAGE, message=message, message_color=message_color)

init_db()
# if __name__ == '__main__':
#     init_db()
#     app.run(host='0.0.0.0', port=5000, debug=False)