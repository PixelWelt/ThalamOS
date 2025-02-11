function openChat() {
    let form = document.getElementById("myForm");
    if (form.style.display === "block") {
        form.style.display = "none";
    } else {
        form.style.display = "block";
    }
}
async function sendMessage(){
    let chatbox = document.getElementById("chatbox");
    let message = document.getElementById("msg").value;
    let button = document.getElementById("chat-send-btn");
    button.enabled = false;
    if(message == ""){
        return;
    }
    let chat = document.createElement("p");
    chat.classList.add("user-chat-message");
    chat.classList.add("chat-message");
    chat.innerHTML = message;
    chatbox.appendChild(chat);
    try {
        const response = await fetch(`${API_URL}/llm/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: message })
    });
        const data = await response.json();
        let answer = document.createElement("p");
        if (data[0] === "Fallback") {
            answer.innerHTML = data[1];
            console.log(data[1]);
        }else if (data[1] === 'error'){
           answer.innerHTML = "Sorry, I couldn't find any items matching your criteria.";
           button.enabled = true;
           console.log("No items found");

        }else{
            //[{"id":35,"position":20,"type":"screw","name":"Screw","info":"{\"bit\": \"PZ2\", \"length\": \"95\", \"diameter\": \"M5\", \"headType\": \"flat\"}","modification_time":null}]
            let answerLen = JSON.parse(data[1]).length;

            data[1] = JSON.parse(data[1]);
            let list = document.createElement("ul");
            for (let i = 0; i < answerLen; i++) {
                if (Array.isArray(data[1]) && data[1].every(item =>
                    typeof item === 'object' && item !== null &&
                    'id' in item && 'position' in item &&
                    'type' in item && 'name' in item &&
                    'info' in item && 'modification_time' in item)) {

                    console.log(`Creating link for item: ${data[1][i].name}`);
                    let listItem = document.createElement("li");
                    listItem.className = "llm-result";
                    let link = document.createElement("a");
                    link.href = `${API_URL}/item/${data[1][i].id}`;
                    link.innerHTML = data[1][i].name;
                    listItem.appendChild(link);
                    list.appendChild(listItem);
                } else {
                    await sendLog('Error','Data structure is not as expected:', data[1][i]);
                }
            }
            answer.appendChild(list);

        }


        answer.classList.add("bot-chat-message");
        answer.classList.add("chat-message");

        chatbox.appendChild(answer);
        chatbox.scrollTop = chatbox.scrollHeight;
        button.enabled = true;
    } catch (error) {
        await sendLog("FATAL", "Error sending message: " + error);
        button.enabled = true;
    }

}
