var send = document.getElementById("send-button");
send.addEventListener("click", sendmessage);
contact = document.getElementById('contact').value;

// setInterval(recievemessage,3000);
// function recievemessage(){
//   let serversidemessage = document.querySelector('.message');
    
//         let xhr1 = new XMLHttpRequest();
//         let url = "/home";
    
//         xhr1.open("POST", url, true);
    
//         xhr1.setRequestHeader("Content-Type", "application/json");
    
//         xhr1.onreadystatechange = function(){
//             if (xhr1.readyState === 4 && xhr1.status === 200){
//                 let s_message = JSON.parse(xhr1.responseText)["content"]["messageList"][0]["message"]
//                 serversidemessage.innerHTML = s_message.value;
//             }
//         };
// }

function sendmessage(){
    var message = document.getElementById("input_message").value;
    var contact = document.getElementById("contact").innerHTML;

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
                    var last_message = document.getElementById("conversation");
                    last_message.innerHTML=`<div><h4>Contact1</h4></div>
                    <div class="ce-chat-subtitle-text"><p>${message}</p></div>
                    <div class="ce-chat-time-text">08:55</div>`;

                    serversidemessage.innerHTML = s_message.value;
                }
                // let s_message = JSON.parse(xhr.responseText)["message"]
                
            }
        };

        var data = JSON.stringify({
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