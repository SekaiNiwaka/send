const socket = io();  // WebSocketの接続を確立

// 接続が成功した時
socket.on("connect", function() {
    console.log("WebSocket connected!");  // 接続成功のメッセージを表示
});

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
