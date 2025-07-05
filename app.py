from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)
os.makedirs('data', exist_ok=True)

def load_data():
    try:
        with open('data/progress.json', 'r') as f:
            return json.load(f)
    except:
        return {"Python": 50, "DBMS": 30, "OS": 20, "AI": 10, "streaks": []}

def save_data(data):
    with open('data/progress.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/update', methods=['POST'])
def update():
    data = load_data()
    subject = request.form['subject']
    progress = int(request.form['progress'])
    data[subject] = progress
    save_data(data)
    return jsonify(success=True)

@app.route('/mark_study', methods=['POST'])
def mark_study():
    data = load_data()
    today = datetime.now().strftime('%Y-%m-%d')
    if today not in data['streaks']:
        data['streaks'].append(today)
    save_data(data)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
