let send = document.getElementById("send-button");
send.addEventListener("click", sendmessage);
contact = document.getElementById('Contactonpage').value;

function original(){
  tabcontent = document.getElementsByClassName("chat-feed");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "block";
  }
  document.getElementById("Contact1").style.display = "none";
  document.getElementById("sid").style.display = "block";
}

let messages = {}

function storeMessages(contact, message, side) {
    
    if(messages[contact]){

        messages[contact].push([message, side])
    } else {

        messages[contact] = [[message, side]]
    }
}

function reRenderMessages(contact) {

    for (let i = 0; i < messages[contact].length; i++) {
      const element = messages[contact][i];
      
      if (element[2]) {
        
        renderMyMessageToScreen(element[1])
      } else {

        renderSendersMessage(element[1])
      }
    }
}

setInterval(recievemessage,3000);

function leave_it(contactName, contact_email){

  
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("ce-conversation");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the link that opened the tab
    let parentdiv = document.getElementById("push-message-block");
    parentdiv.innerHTML = ""

    let title = document.getElementById("Contactonpage")
    title.innerHTML = contactName
    
}

function recieve_contacts(){
    let xhr1 = new XMLHttpRequest();
    let url = "/home";

    xhr1.open("POST", url, true);

    xhr1.setRequestHeader("Content-Type", "application/json");

    xhr1.onreadystatechange = function(){

        if (xhr1.readyState === 4 && xhr1.status === 200){

            console.log(xhr1.responseText)
            contactList = JSON.parse(xhr1.responseText)["contactList"]

            for (let i = 0; i < contactList.length; i++) {
                
                let element = contactList[i];

                contact = element
                let time = new Date(),
                h = (time.getHours()<10?'0':'') + time.getHours(),
                m = (time.getMinutes()<10?'0':'') + time.getMinutes();
                let j = h + ':' + m;

                const parentdiv = document.getElementById("ce-active-chat-card");
                console.log(parentdiv.innerHTML)
                let newdiv = document.createElement("new_contact");
                newdiv.id = "new_contact"
                newdiv.innerHTML = `<div id="conversation" onclick = "leave_it('${contact}','gmail.com')">
                <div><h4>${contact}</h4></div>
                <div class="ce-chat-subtitle-text"><p>last Message</p></div>
                <div class="ce-chat-time-text">${j}</div>
                </div>`

                parentdiv.append(newdiv);
            }
        }
    };

    
    let contact = JSON.stringify({
        "requestPurpose": "getContactList",
        "content": {
            "token": localStorage.getItem("token")
        }
    });

    console.log(contact);
    xhr1.send(contact);
}

recieve_contacts()

function renderSendersMessage(message){

    const maindiv = document.getElementById("push-message-block");
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
    last_message.innerHTML=`<div><h4 id="Contact">sid</h4></div>
    <div class="ce-chat-subtitle-text"><p>${message}</p></div>
    <div class="ce-chat-time-text">08:55</div>`;
}

function renderMyMessageToScreen(message) {

    const maindiv = document.getElementById("push-message-block");
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
                storeMessages(document.getElementById("Contact").innerHTML, message, 1)
            }
        }
    };

    let data = JSON.stringify({

        "requestPurpose": "messageRecieve",
        "content": {
            "token": localStorage.getItem("token"),
        },
        "sender": document.getElementById("Contactonpage").innerHTML
    })
    
    console.log(data);
    xhr.send(data);
}

function sendmessage(){
    let message = document.getElementById("input_message").value;
    let contact = document.getElementById("Contactonpage").innerHTML;

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
                    storeMessages(contact, message, 0)
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