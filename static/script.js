const socket = io();  // WebSocketの接続を確立

// メッセージを送信
function sendMessage() {
    let message = document.getElementById("input-text").value;
    socket.emit("send_post", { text: message });  // サーバーに送信
    document.getElementById("input-text").value = "";  // 入力欄をクリア
}

// サーバーから最新の投稿を受信し、画面を更新
socket.on("update_post", function(data) {
    document.getElementById("display-area").innerText = data.text;
});
