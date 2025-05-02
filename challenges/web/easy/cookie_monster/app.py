from flask import Flask, render_template, make_response, request

app = Flask(__name__)

@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    resp.set_cookie('role', 'guest')
    return resp

@app.route('/admin')
def admin():
    role = request.cookies.get('role')
    if role == 'admin':
        return 'FLAG{cookie_monster_loves_admin_cookies}'
    return 'Access Denied'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)