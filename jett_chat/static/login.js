function setToken(token){ 
    
    console.log(token);                              // debug
    localStorage.setItem("token", token)             // store token value
    document.location.href = "/home"
}

function sendJSON(){
    let uname = document.querySelector('#uname');
    let password = document.querySelector('#password');

    let url = "/login";
    let token;

    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function(){
        if (xhr.readyState === 4 && xhr.status === 200){
            token = JSON.parse(xhr.responseText)["token"]
            setToken(token);
        }
    };

    var data = JSON.stringify({"uname": uname.value, "password": password.value});
    xhr.send(data);
    
    // to empty the input boxes
    document.querySelector("#uname").value="";
    document.querySelector("#password").value="";
}