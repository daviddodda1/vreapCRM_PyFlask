function validate() {
    if($('#userPhoneNumber').val() == ''){
        $("#EmailField").addClass('addBorder')
    }
    if($('#userPassword').val() == ''){
        $("#PasswordField").addClass('addBorder')
    }
}

$("#submitBtn").click(function(){
    validate();
    var da = {
        "user_ID": $('#userPhoneNumber').val(),
        "userPassword": $('#userPassword').val(),
    }
    console.log(da);
    $.ajax({
        type: 'POST',
        data: JSON.stringify(da),
        contentType: 'application/json',
        url: 'http://localhost:5000/login',
        success: function(data) {
            if(data == "User phone number and Password dosent match"){
                swal("Login Error", "User phone number and Password dosent match", "error");
            } else{
                if(data == "no user exists"){
                    swal("Login Error", "User does not exists", "error");
                } else {
                    swal("Login Successful", "please wait wile we redirect you.", "success");
                    document.cookie = "jwt =" + data + ";";
                    setTimeout(redirect(), 6000);
                    console.log(getCookie("jwt"));
                }
            }
        }
    })
})

function redirect(){
    window.location.replace("http://localhost:5500/mainPage.html");
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
}





