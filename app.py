from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# データベース初期化
def init_db():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS messages 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      content TEXT NOT NULL, 
                      timestamp TEXT NOT NULL)''')
        conn.commit()

# 最新10件のメッセージを取得
def get_latest_messages():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute("SELECT content, timestamp FROM messages ORDER BY timestamp DESC LIMIT 10")
        result = c.fetchall()
    return [{'content': row[0], 'timestamp': row[1]} for row in result] if result else []

# メッセージ保存
def save_message(content):
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO messages (content, timestamp) VALUES (?, ?)", 
                  (content, datetime.now().isoformat()))
        conn.commit()

@app.route('/')
def index():
    messages = get_latest_messages()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    content = request.form['content']
    save_message(content)
    return jsonify({'status': 'success', 'message': content})

@app.route('/update', methods=['GET'])
def update():
    messages = get_latest_messages()
    return jsonify({'messages': messages})

# アプリケーション起動時にデータベースを初期化
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)