from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2 import pool
from datetime import datetime
import os

app = Flask(__name__)

# PostgreSQL接続プール設定
db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # 最小・最大接続数
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

# データベース初期化
def init_db():
    conn = db_pool.getconn()
    try:
        with conn.cursor() as c:
            c.execute('''CREATE TABLE IF NOT EXISTS messages 
                         (id SERIAL PRIMARY KEY, 
                          content TEXT NOT NULL, 
                          timestamp TEXT NOT NULL)''')
            conn.commit()
    finally:
        db_pool.putconn(conn)

# 最新10件のメッセージを取得
def get_latest_messages():
    conn = db_pool.getconn()
    try:
        with conn.cursor() as c:
            c.execute("SELECT content, timestamp FROM messages ORDER BY timestamp DESC LIMIT 10")
            result = c.fetchall()
        return [{'content': row[0], 'timestamp': row[1]} for row in result] if result else []
    finally:
        db_pool.putconn(conn)

# メッセージ保存
def save_message(content):
    conn = db_pool.getconn()
    try:
        with conn.cursor() as c:
            c.execute("INSERT INTO messages (content, timestamp) VALUES (%s, %s)", 
                      (content, datetime.now().isoformat()))
            conn.commit()
    finally:
        db_pool.putconn(conn)

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