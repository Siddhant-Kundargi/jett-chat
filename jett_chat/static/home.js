let send = document.getElementById("send-button");
send.addEventListener("click", sendmessage);
contact = document.getElementById('contact').value;

setInterval(recievemessage,3000);
function renderSendersMessage(message){

    const maindiv = document.getElementById("message-pad");
    let userdiv = document.createElement("div");
    userdiv.id = "user";
    userdiv.innerHTML = `</div>
             <div class="message-pad" id="message-pad">
              <div class="message-row" id="message-row">
                <div class="message-block" id="message-block">
                    <img src="avatar3.jpg" width="44px" height="44px" class="message-avatar">
                  <div class="message" id="message" name="message">
                    <p>${message}</p>
                  </div>
                </div>
            </div>`

    maindiv.appendChild(userdiv);
    let last_message = document.getElementById("conversation");
    last_message.innerHTML=`<div><h4 id="contact">sid</h4></div>
    <div class="ce-chat-subtitle-text"><p>${message}</p></div>
    <div class="ce-chat-time-text">08:55</div>`;
}

function renderMyMessageToScreen(message) {

    const maindiv = document.getElementById("message-pad");
    let userdiv = document.createElement("div");
    userdiv.id = "user";
    userdiv.innerHTML = `<div class="message-row">
            <div class="message-block-myside">
                <div class="message-myside" id="message-myside">
                    <span>${message}</span>
                </div>
            </div>
        </div>`;
    maindiv.appendChild(userdiv);
    let last_message = document.getElementById("conversation");
    last_message.innerHTML=`<div><h4 id="contact">sid</h4></div>
    <div class="ce-chat-subtitle-text"><p>${message}</p></div>
    <div class="ce-chat-time-text">08:55</div>`;
}

function recievemessage(){

    let xhr = new XMLHttpRequest();
    let url = "/home";

    xhr.open("POST", url, true);

    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function(){

        if (xhr.readyState === 4 && xhr.status === 200){
            let message_list = JSON.parse(xhr.responseText)["messageList"]

            console.log(message_list)
            
            for (let i = 0; i < message_list.length; i++) {

                let message = message_list[i];

                console.log(message)
                renderSendersMessage(message)
            }
        }
    };

    let data = JSON.stringify({

        "requestPurpose": "messageRecieve",
        "token": localStorage.getItem("token"),
        "sender": document.getElementById("contact").innerHTML
    })
    
    console.log(data);
    xhr.send(data);
}

function sendmessage(){
    let message = document.getElementById("input_message").value;
    let contact = document.getElementById("contact").innerHTML;

    if(!message){
        alert("Please type message before sending");

    } else {
      
        let serversidemessage = document.querySelector('.message');
        let input_message = document.querySelector('#input_message');
    
        let xhr = new XMLHttpRequest();
        let url = "/home";
    
        xhr.open("POST", url, true);
    
        xhr.setRequestHeader("Content-Type", "application/json");
    
        xhr.onreadystatechange = function(){
            if (xhr.readyState === 4 && xhr.status === 200){

                if (xhr.responseText == "200"){

                    renderMyMessageToScreen(message)
                } 
            }
        };

        let data = JSON.stringify({
          "requestPurpose": "messageSend",
          "content": {
      
            "token": localStorage.getItem("token"),
      
                "messageList": [
                    {
                      "reciever": contact,
                      "message": input_message.value
                    }
                ]
            }
        });
      
        console.log(data);
    
        xhr.send(data);
        document.getElementById("input_message").value="";
    }
}