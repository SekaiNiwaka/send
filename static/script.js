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
            document.getElementById('message-input').value = '';
            updateMessages(); // 送信後に即時更新
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('update-btn').addEventListener('click', function() {
    updateMessages();
});

function updateMessages() {
    fetch('/update')
    .then(response => response.json())
    .then(data => {
        const messageList = document.getElementById('message-display');
        messageList.innerHTML = ''; // 既存の内容をクリア
        data.messages.forEach(msg => {
            const li = document.createElement('li');
            li.textContent = `${msg.timestamp}: ${msg.content}`;
            messageList.appendChild(li);
        });
    })
    .catch(error => console.error('Error:', error));
}