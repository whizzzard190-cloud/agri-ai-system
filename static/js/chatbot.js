function sendMessage() {
    let msg = document.getElementById("msg").value;

    fetch("/chatbot", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "message=" + msg
    })
    .then(res => res.text())
    .then(data => {
        document.getElementById("response").innerText = data;
    });
}