// 送信処理
document.getElementById('submit-btn').addEventListener('click', function() {
    const content = document.getElementById('message-input').value;
    if (content.trim() === '') return;

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `content=${encodeURIComponent(content)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('message-input').value = ''; // 入力クリア
        }
    })
    .catch(error => console.error('Error:', error));
});

// リアルタイム更新（SSE）
const source = new EventSource('/stream');
source.onmessage = function(event) {
    const data = JSON.parse(event.data);
    document.getElementById('message-display').textContent = data.message;
};
source.onerror = function() {
    console.error('SSE connection error');
};