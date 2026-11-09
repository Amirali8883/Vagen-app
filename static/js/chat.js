(function () {
    const config = window.chatConfig;
    const messages = document.getElementById("messages");
    const form = document.getElementById("message-form");
    const input = document.getElementById("message");
    const error = document.getElementById("chat-error");
    const socket = io();

    function showError(message) {
        error.textContent = message;
        error.hidden = false;
    }

    function renderMessage(message) {
        const item = document.createElement("p");
        item.textContent = `${message.sender_id}: ${message.content}`;
        messages.appendChild(item);
    }

    fetch(config.historyUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error("Kunne ikke hente meldinger.");
            }
            return response.json();
        })
        .then(history => history.forEach(renderMessage))
        .catch(loadError => showError(loadError.message));

    socket.on("connect", function () {
        socket.emit("join_room", {
            recipient_id: config.recipientUsername
        });
    });

    socket.on("private_message", renderMessage);
    socket.on("chat_error", data => showError(data.message));

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const content = input.value.trim();
        if (!content) {
            return;
        }

        socket.emit("send_private_message", {
            recipient_id: config.recipientUsername,
            content: content
        });
        input.value = "";
    });
})();
