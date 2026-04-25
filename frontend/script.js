async function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value;

    if (!message) return;

    addUserMessage(message);
    input.value = "";

    const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    });

    const data = await response.json();
    addBotMessage(formatResponse(data.response));
}

/* USER MESSAGE */
function addUserMessage(text) {
    const chatBox = document.getElementById("chat-box");

    const div = document.createElement("div");
    div.className = "user-msg";
    div.innerHTML = text;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* BOT MESSAGE (CARD STYLE) */
function addBotMessage(text) {
    const chatBox = document.getElementById("chat-box");

    const div = document.createElement("div");
    div.className = "bot-msg";
    div.innerHTML = text;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* 🔥 FORMAT RESPONSE INTO CLEAN UI */
function formatResponse(text) {

    // Convert bullet points
    text = text.replace(/\n/g, "<br>");

    // Highlight headings
    text = text.replace(/(CGPA|required|GRE|TOEFL|Admission|Chance)/gi, "<b>$1</b>");

    return text;
}