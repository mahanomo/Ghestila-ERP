console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

function onlineUsersSelectorAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsersSelector.appendChild(newOption);
}

function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

// focus input on load
chatMessageInput.focus();

// send message on enter
chatMessageInput.onkeyup = function (e) {
    if (e.keyCode === 13) {
        chatMessageSend.click();
    }
};

let chatSocket = null;

function connect() {
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");

    chatSocket.onopen = function () {
        console.log("Successfully connected to the WebSocket.");
    };

    chatSocket.onclose = function () {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(connect, 2000);
    };

    chatSocket.onerror = function (err) {
        console.error("WebSocket encountered an error: ", err.message);
        chatSocket.close();
    };

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);

        switch (data.type) {
            case "chat_message":
                chatLog.value += data.user + ": " + data.message + "\n";
                break;

            case "user_list":
                data.users.forEach(user => onlineUsersSelectorAdd(user));
                break;

            case "user_join":
                chatLog.value += data.user + " joined the room.\n";
                onlineUsersSelectorAdd(data.user);
                break;

            case "user_leave":
                chatLog.value += data.user + " left the room.\n";
                onlineUsersSelectorRemove(data.user);
                break;

            default:
                console.error("Unknown message type:", data.type);
        }

        chatLog.scrollTop = chatLog.scrollHeight;
    };
}

connect();

chatMessageSend.onclick = function () {
    const message = chatMessageInput.value.trim();
    if (message.length === 0 || !chatSocket || chatSocket.readyState !== WebSocket.OPEN) return;

    chatSocket.send(JSON.stringify({
        "message": message
    }));
    chatMessageInput.value = "";
};