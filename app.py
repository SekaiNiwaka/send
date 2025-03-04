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

# 最新メッセージ取得
def get_latest_message():
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute("SELECT content FROM messages ORDER BY timestamp DESC LIMIT 1")
        result = c.fetchone()
    return result[0] if result else "まだ投稿がありません"

# メッセージ保存
def save_message(content):
    with sqlite3.connect('messages.db') as conn:
        c = conn.cursor()
        c.execute("INSERT INTO messages (content, timestamp) VALUES (?, ?)", 
                  (content, datetime.now().isoformat()))
        conn.commit()

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

# アプリケーション起動時にデータベースを初期化
init_db()  # これを追加して、起動時に必ず実行

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)