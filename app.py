from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# データベース初期化
def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  content TEXT NOT NULL, 
                  timestamp TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# 最新メッセージ取得
def get_latest_message():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("SELECT content FROM messages ORDER BY timestamp DESC LIMIT 1")
    result = c.fetchone()
    conn.close()
    return result[0] if result else "まだ投稿がありません"

# メッセージ保存
def save_message(content):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (content, timestamp) VALUES (?, ?)", 
              (content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html', message=get_latest_message())

@app.route('/submit', methods=['POST'])
def submit():
    content = request.form['content']
    save_message(content)
    return jsonify({'status': 'success', 'message': content})

@app.route('/update', methods=['GET'])
def update():
    return jsonify({'message': get_latest_message()})

# ローカル開発用のみ実行
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)