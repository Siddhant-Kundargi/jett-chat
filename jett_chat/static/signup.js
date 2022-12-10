function sendJSONdet(){
    let full_name   = document.querySelector('#full_name');
    let user_name   = document.querySelector('#user_name');
    let password_s  = document.querySelector('#password_s');
    let password_c  = document.querySelector('#password_c');
    let email       = document.querySelector('#email');
    // let phone       = document.querySelector('#phone');


    if (password_s.value != password_c.value) {

        window.alert("The Confirm Password is not same as original password!");
        
    } else {

        let xhr = new XMLHttpRequest();
        let url = "/register";

        xhr.open("POST", url, true);

        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function(){
            if (xhr.readyState === 4 && xhr.status === 200){
                
                let result = this.responseText;
                if(result == "User Created"){
                    document.location.href = "/login"
                }
            }
        };

        var data = JSON.stringify({"name": full_name.value, "uname": user_name.value, "password": password_s.value, "email": email.value, "phone": "01012031023"});
        console.log(data);

        xhr.send(data);
    }
     
}