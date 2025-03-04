document.getElementById('submit-btn').addEventListener('click', function() {
    const content = document.getElementById('message-input').value;
    if (content.trim() === '') return;

    console.log('Sending message:', content); // デバッグ用
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `content=${encodeURIComponent(content)}`
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response:', data); // デバッグ用
        if (data.status === 'success') {
            document.getElementById('message-input').value = '';
            updateMessage();
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('update-btn').addEventListener('click', function() {
    console.log('Updating message'); // デバッグ用
    updateMessage();
});

function updateMessage() {
    fetch('/update')
    .then(response => response.json())
    .then(data => {
        console.log('Updated message:', data.message); // デバッグ用
        document.getElementById('message-display').textContent = data.message;
    })
    .catch(error => console.error('Error:', error));
}