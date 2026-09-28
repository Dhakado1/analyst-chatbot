document.addEventListener("DOMContentLoaded", () => {
    const chatMsgs = document.getElementById("chat-messages");
    const input = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const debugSql = document.getElementById("debug-sql");

    function addMessage(text, sender) {
        const div = document.createElement("div");
        div.className = `message ${sender}`;
        div.innerHTML = `<div class="bubble">${text}</div>`;
        chatMsgs.appendChild(div);
        chatMsgs.scrollTop = chatMsgs.scrollHeight;
    }

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;
        addMessage(text, "user");
        input.value = "";
        
        addMessage("Typing...", "assistant loading");
        
        try {
            const res = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });
            const data = await res.json();
            
            document.querySelector(".loading").remove();
            addMessage(data.error || data.response, "assistant");
            debugSql.innerText = data.sql || "No SQL generated.";
        } catch (e) {
            document.querySelector(".loading").remove();
            addMessage("Network error.", "assistant");
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    input.addEventListener("keypress", (e) => e.key === "Enter" && sendMessage());
    
    document.getElementById("clear-btn").addEventListener("click", async () => {
        await fetch("/clear", { method: "POST" });
        chatMsgs.innerHTML = `<div class="message assistant"><div class="bubble">Context cleared.</div></div>`;
        debugSql.innerText = "No SQL generated yet.";
    });
});