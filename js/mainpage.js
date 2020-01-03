
var searchNumber;

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
                $("#mainComtainer").html(data)
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
        $("#"+a_ID+"mainComtainer").removeClass("col-md-12");
        $("#"+a_ID+"mainComtainer").addClass("col-md-6");
        $("#"+a_ID+"mainComtainer").removeClass("col-sm-12");
        $("#"+a_ID+"mainComtainer").addClass("col-sm-12");
        $("#"+a_ID+"secContainer").removeClass("NoDisplay");
        $("#"+a_ID+"secContainer").removeClass("col-md-0");        
        $("#"+a_ID+"secContainer").addClass("col-md-6");
        $("#"+a_ID+"secContainer").removeClass("col-sm-0");        
        $("#"+a_ID+"secContainer").addClass("col-sm-12");
        $("#"+a_ID).attr('val',1);
        $("#"+a_ID).html("Show less");
    } else {
        temp.parent().removeClass("col-sm-12");
        temp.parent().removeClass("col-md-12");
        temp.parent().addClass("col-sm-6");
        temp.parent().addClass("col-md-4");
        $("#"+a_ID+"mainComtainer").removeClass("col-md-6");
        $("#"+a_ID+"mainComtainer").addClass("col-md-12");
        $("#"+a_ID+"mainComtainer").removeClass("col-sm-12");
        $("#"+a_ID+"mainComtainer").addClass("col-sm-12");
        $("#"+a_ID+"secContainer").addClass("NoDisplay");
        $("#"+a_ID+"secContainer").removeClass("col-md-6");
        $("#"+a_ID+"secContainer").addClass("col-md-0");        
        $("#"+a_ID+"secContainer").removeClass("col-sm-12");
        $("#"+a_ID+"secContainer").addClass("col-sm-0");        
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


function SerchData(){

    var searchVal = $('#SerchInput').val();
    var cooky = getCookie("jwt");
    da = {
        'searchPhoneNo': searchVal,
        'cookie': cooky
    }
    console.log(da)
    $.ajax({
        type: 'POST',
        data: JSON.stringify(da),
        contentType: 'application/json',
        url: 'http://localhost:5000/searchNo',
        success: function(data) {
            if(data == "relogin"){
                window.location.replace("http://localhost:5500/index.html");
            } else{
                if(data == "No Entry"){
                    swal("Phone Number Error", "No Entry With That Phone Number", "error");
                }else{
                    searchNumber = searchVal;
                    $("#userCallContainer").remove();
                    $("#SerchContainer").removeClass("NoDisplay");
                    $("#SerchContainer").html(data);
                }
            }
        }
    })

}


function SaveCallData(){
    var cooky = getCookie("jwt");
    if(validateForm()){
        da = {
            "callNumber": searchNumber,
            "Call_Status": $("#inputCall_Status").val(),
            "Why_Register": $("#inputWhy_Register").val(),
            "Potantial": $("#inputPotantial").val(),
            "What_Discussed": $("#inputWhat_Discussed").val(),
            "Whatsapp_Number": $("#inputWhatsapp_Number").val(),
            "Whatsapp_sent": $("#inputWhatsapp_sent").val(),
            "is_Followup_Needed": $("#inputis_Followup_Needed").val(),
            "FollowUp_Instructions": $("#inputFollowUp_Instructions").val(),
            "cooky": cooky
        }
        console.log(da)
        $.ajax({
            type: 'POST',
            data: JSON.stringify(da),
            contentType: 'application/json',
            url: 'http://localhost:5000/addCallData',
            success: function(data) {
                if(data == "login"){
                    window.location.replace("http://localhost:5500/index.html");
                } else{
                    if(data == "Data Saved"){
                        swal("Call Data Saved", "the call entry had been saved", "success");
                        setTimeout(reloadPage(), 6000);
                    }
                }
            }
        })
    }
}

function reloadPage(){
    location.reload(true);
}

function validateForm(){
    var temp = true;
    if($("#inputCall_Status").val() == ""){
        temp = false;
        $("#inputCall_Status").addClass('is-invalid');
    }
    if($("#inputWhy_Register").val() == ""){
        temp = false;
        $("#inputWhy_Register").addClass('is-invalid');
    }
    if($("#inputPotantial").val() == ""){
        temp = false;
        $("#inputPotantial").addClass('is-invalid');
    }
    if($("#inputWhat_Discussed").val() == ""){
        temp = false;
        $("#inputWhat_Discussed").addClass('is-invalid');
    }
    if($("#inputWhatsapp_Number").val() == ""){
        temp = false;
        $("#inputWhatsapp_Number").addClass('is-invalid');
    }
    if($("#inputWhatsapp_sent").val() == ""){
        temp = false;
        $("#inputWhatsapp_sent").addClass('is-invalid');
    }
    if($("#inputis_Followup_Needed").val() == ""){
        temp = false;
        $("#inputis_Followup_Needed").addClass('is-invalid');   
    }
    if($("#inputFollowUp_Instructions").val() == ""){
        temp = false;
        $("#inputFollowUp_Instructions").addClass('is-invalid');
    }

    if(temp){
        $("#inputCall_Status").addClass('is-valid');
        $("#inputCall_Status").removeClass('is-invalid');
        $("#inputWhy_Register").addClass('is-valid');
        $("#inputWhy_Register").removeClass('is-invalid');
        $("#inputPotantial").addClass('is-valid');
        $("#inputPotantial").removeClass('is-invalid');

        $("#inputWhat_Discussed").addClass('is-valid');
        $("#inputWhat_Discussed").removeClass('is-invalid');

        $("#inputWhatsapp_Number").addClass('is-valid');
        $("#inputWhatsapp_Number").removeClass('is-invalid');

        $("#inputWhatsapp_sent").addClass('is-valid');
        $("#inputWhatsapp_sent").removeClass('is-invalid');

        $("#inputis_Followup_Needed").addClass('is-valid');
        $("#inputis_Followup_Needed").removeClass('is-invalid');

        $("#inputFollowUp_Instructions").addClass('is-valid');
        $("#inputFollowUp_Instructions").removeClass('is-invalid');

        return temp;
    }else{
        return temp;
    }
}




