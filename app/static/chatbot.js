function openChat() {
    var form = document.getElementById("myForm");
    if (form.style.display === "block") {
        form.style.display = "none";
    } else {
        form.style.display = "block";
    }
}
function sendMessage(){
    var chatbox = document.getElementById("chatbox");
    var message = document.getElementById("msg").value;
    if(message == ""){
        return;
    }
    var chat = document.createElement("p");
    chat.classList.add("user-chat-message");
    chat.classList.add("chat-message");
    chat.innerHTML = message;
    chatbox.appendChild(chat);
    setTimeout(function() {
        var answer = document.createElement("p");
        answer.classList.add("bot-chat-message");
        answer.classList.add("chat-message");
        answer.innerHTML = "This is a delayed response.";
        chatbox.appendChild(answer);
    }, 1000);
}
