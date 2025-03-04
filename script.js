function updateMessageDisplay() {
    fetch('/get_message')
        .then(response => response.json())
        .then(data => {
            document.getElementById('messageDisplay').textContent = data.content;
        });
}

document.getElementById('sendButton').addEventListener('click', () => {
    const message = document.getElementById('messageInput').value;
    if (message) {
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: message }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                document.getElementById('messageInput').value = '';
                updateMessageDisplay();
            }
        });
    }
});

updateMessageDisplay();
