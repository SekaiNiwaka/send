from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import sqlite3
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # WebSocketの設定

# データベースの初期化
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)''')
    conn.commit()
    conn.close()

# 最新の投稿を取得
def get_latest_post():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT text FROM posts ORDER BY id DESC LIMIT 1")
    post = c.fetchone()
    conn.close()
    return post[0] if post else "まだ投稿がありません"

# 投稿を保存
def save_post(text):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO posts (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html", post=get_latest_post())

# クライアントから投稿を受信したときの処理
@socketio.on("send_post")
def handle_post(data):
    text = data["text"]
    save_post(text)  # データベースに保存
    latest_post = get_latest_post()
    
    # 全クライアントに最新の投稿を送信（リアルタイム更新）
    emit("update_post", {"text": latest_post}, broadcast=True)

if __name__ == "__main__":
    init_db()  # サーバー起動時にDBを作成
    PORT = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=PORT, debug=True)
