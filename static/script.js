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
            updateMessage(); // 送信後に即時更新
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('update-btn').addEventListener('click', function() {
    updateMessage();
});

function updateMessage() {
    fetch('/update')
    .then(response => response.json())
    .then(data => {
        document.getElementById('message-display').textContent = data.message;
    })
    .catch(error => console.error('Error:', error));
}