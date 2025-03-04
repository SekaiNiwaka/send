var socket = io.connect(window.location.hostname);

// 新しい投稿が送信されるとき
socket.on('new_post', function(data) {
    document.getElementById('display-area').innerText = data.text;
});

function sendMessage() {
    let message = document.getElementById("input-text").value;
    fetch("/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: message })
    }).then(() => {
        document.getElementById("input-text").value = ''; // 入力フィールドをリセット
    });
}
