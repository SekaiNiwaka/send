function sendMessage() {
    let message = document.getElementById("input-text").value;
    fetch("/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: message })
    }).then(() => {
        location.reload();  // 送信後にページをリロード
    });
}
