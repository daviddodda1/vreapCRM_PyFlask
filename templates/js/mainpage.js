
$( document ).ready(function() {
    var cooky = getCookie("jwt");
    da = {
        "cookie": cooky
    }
    console.log(cooky);
    $.ajax({
        type: 'POST',
        data: JSON.stringify(da),
        contentType: 'application/json',
        url: 'http://localhost:5000/userAuth',
        success: function(data) {
            if(data == "login"){
                window.location.replace("http://localhost:5500/index.html");
            } else{

                console.log("User main Page");
            }
        }
    })

});

function showData(a_ID){
    var temp = $("#"+a_ID).parent().parent();
    console.log("button Press " + $("#"+a_ID).attr('val'));
    if($("#"+a_ID).attr('val') == 0){
        temp.parent().removeClass("col-sm-6");
        temp.parent().removeClass("col-md-4");
        temp.parent().addClass("col-sm-12");
        temp.parent().addClass("col-md-12");
        $("#"+a_ID+"mainComtainer").removeClass("col-12");
        $("#"+a_ID+"mainComtainer").addClass("col-6");
        $("#"+a_ID+"secContainer").removeClass("col-0");        
        $("#"+a_ID+"secContainer").addClass("col-6");
        $("#"+a_ID).attr('val',1);
        $("#"+a_ID).html("Show less");
    } else {
        temp.parent().removeClass("col-sm-12");
        temp.parent().removeClass("col-md-12");
        temp.parent().addClass("col-sm-6");
        temp.parent().addClass("col-md-4");
        $("#"+a_ID+"mainComtainer").removeClass("col-6");
        $("#"+a_ID+"mainComtainer").addClass("col-12");
        $("#"+a_ID+"secContainer").removeClass("col-6");
        $("#"+a_ID+"secContainer").addClass("col-0");
        $("#"+a_ID).attr('val',0);
        $("#"+a_ID).html("Show More");
    }
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