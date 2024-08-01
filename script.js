// script.js

const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input button");
const chatbox = document.querySelector(".chatbox");

let userMessage;

const createChatLi = (message, className) => {
    const chatLi = document.createElement("div");
    chatLi.classList.add("chat", className);
    chatLi.innerHTML = `<div class="message"><p>${message}</p></div>`;
    
    return chatLi;
};

const createProfileBot = () => {
    const profile = document.createElement("div");
    profile.classList.add("chatbox-logo");
    profile.innerHTML = `<img src="./logoLight.jpg" alt="Logo ChatBot"
						class="logo">
					<span>ChatBot</span>`;
    return profile
}

const createProfileUser = () => {
    const profile = document.createElement("div");
    profile.classList.add("chatbox-logo");
    profile.innerHTML = `<span>Vous</span>`;
    return profile
}

const generateResponse = (incomingChatLi) => {
    const API_URL = "http://127.0.0.1:8000/ask";
    const messageElement = incomingChatLi.querySelector("p");
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            prompt: userMessage,
        }),
    };

    fetch(API_URL, requestOptions)
        .then((res) => {
            if (!res.ok) {
                throw new Error("Network response was not ok");
            }
            return res.json();
        })
        .then((data) => {
            messageElement.textContent = data.answer;

            const rightDiv = document.createElement("div");
            rightDiv.classList.add("right");

            // rightDiv.innerHTML =
            //     `<img class="result-img" src="http://127.0.0.1:8000/data1" width="200"/><img class="result-img" src="http://127.0.0.1:8000/data2" width="200"/>`;

            
            
            data.sources.forEach(source => {
                const p = document.createElement("p")
                p.classList.add("source")   
                p.innerHTML = source
                rightDiv.append(p)
            });

            incomingChatLi.append(rightDiv)
        })
        .catch((error) => {
            messageElement.classList.add("error");
            messageElement.textContent =
                "Oups ! Quelque chose s'est mal passé. Veuillez réessayer, s'il vous plaît !";
        })
        .finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
};

const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) {
        return;
    }
    chatInput.value = "";
    const outgoingChatLi = createChatLi(userMessage, "chat-outgoing")
    outgoingChatLi.append(createProfileUser());
    chatbox.appendChild(outgoingChatLi);
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        const incomingChatLi = createChatLi("......", "chat-incoming");
        chatbox.appendChild(createProfileBot())
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
};

sendChatBtn.addEventListener("click", handleChat);

document.addEventListener("keyup", function(event) {
    if (event.key === "Enter") {
        handleChat();
    }
  });