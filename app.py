from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('messages.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.before_first_request
def init_db():
    with app.app_context():
        conn = get_db()
        conn.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()

@app.route('/get_message', methods=['GET'])
def get_message():
    conn = get_db()
    cursor = conn.execute('SELECT content FROM messages ORDER BY timestamp DESC LIMIT 1')
    message = cursor.fetchone()
    if message:
        return jsonify({'content': message['content']})
    return jsonify({'content': ''})

@app.route('/send_message', methods=['POST'])
def send_message():
    content = request.json.get('content')
    if content:
        conn = get_db()
        conn.execute('INSERT INTO messages (content) VALUES (?)', (content,))
        conn.commit()
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'No content provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
