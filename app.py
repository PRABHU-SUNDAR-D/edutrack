from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os, json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to something secure

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load users from file
def load_users():
    try:
        with open('data/users.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Load progress for current user
def load_progress(username):
    path = f'data/{username}.json'
    if not os.path.exists(path):
        return {"Python": 50, "DBMS": 30, "OS": 20, "AI": 10, "streaks": []}
    with open(path, 'r') as f:
        return json.load(f)

def save_progress(username, data):
    with open(f'data/{username}.json', 'w') as f:
        json.dump(data, f, indent=4)

# User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Routes

@app.route('/')
@login_required
def index():
    data = load_progress(current_user.id)
    return render_template('index.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            login_user(User(username))
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error='Username already exists')
        users[username] = {'password': password}
        save_users(users)
        os.makedirs('data', exist_ok=True)
        save_progress(username, {"Python": 0, "DBMS": 0, "OS": 0, "AI": 0, "streaks": []})
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/update', methods=['POST'])
@login_required
def update():
    data = load_progress(current_user.id)
    subject = request.form['subject']
    progress = int(request.form['progress'])
    data[subject] = progress
    save_progress(current_user.id, data)
    return '', 204

@app.route('/mark_study', methods=['POST'])
@login_required
def mark_study():
    data = load_progress(current_user.id)
    today = datetime.now().strftime('%Y-%m-%d')
    if today not in data['streaks']:
        data['streaks'].append(today)
    save_progress(current_user.id, data)
    return '', 204

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)

    app.run(host='0.0.0.0', port=10000)
