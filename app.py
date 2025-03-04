from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)

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

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    save_post(data["text"])
    return jsonify({"status": "success", "message": "投稿を保存しました"})

# 最新の投稿を返すエンドポイント
@app.route("/latest")
def latest():
    post = get_latest_post()
    return jsonify({"text": post})

if __name__ == "__main__":
    init_db()  # サーバー起動時にDBを作成
    app.run(host="0.0.0.0", port=5000, debug=True)
