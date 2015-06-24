function validate_register_form ( )
{
    valid = true;

        if ( document.register_form.login.value == "" )
        {
            document.getElementById("failName").className = "";
            valid = false;
        }
        else{
            document.getElementById("failName").className = "none";
        }

        if ( document.register_form.inEmail.value == "" )
        {
            document.getElementById("failEmail").className = "";
            valid = false;
        }
        else{
            document.getElementById("failEmail").className = "none";
        }

        if ( (document.register_form.password.value != document.register_form.repeatPassword.value) || document.register_form.password.value == "")
        {
            document.getElementById("correctPass").className = "";
            document.getElementById("correctPass2").className = "";
            valid = false;
        }
        else{
            document.getElementById("correctPass").className = "none";
            document.getElementById("correctPass2").className = "none";
        }
    return valid;
}

function validate_login_form ( )
{
    valid = true;

        if ( document.login_form.username.value == "" )
        {
            document.getElementById("logName").className = "";
            valid = false;
        }
        else{
            document.getElementById("logName").className = "none";
        }


        if ( document.login_form.password.value == "" )
        {
            document.getElementById("logPass").className = "";
            valid = false;
        }
        else{
            document.getElementById("logPass").className = "none";
        }

    return valid;
}


function validate_ask ( )
{
    valid = true;

        if ( document.ask_form.titleAsk.value == "" )
        {
            document.getElementById("titleName").className = "";
            valid = false;
        }
        else{
            document.getElementById("titleName").className = "none";
        }


        if ( document.ask_form.contentAsk.value == "" )
        {
            document.getElementById("askContent").className = "";
            valid = false;
        }
        else{
            document.getElementById("askContent").className = "none";
        }

        if ( document.ask_form.tagsAsk.value == "" )
        {
            document.getElementById("tagsAskId").className = "";
            valid = false;
        }
        else{
            document.getElementById("tagsAskId").className = "none";
        }
    return valid;
}

//function login(){
//    if( validate_login_form() ){
//        login = $("#loginName").val();
//        password = $("#controlPassword").val();
//        $.ajax({
//        url : "/register/",
//        type: "post",
//        data:{
//            'username': login,
//            'password': password,
//            },
//        success: function(json){
//                    if(json == 'ok'){
//                        location.reload();
//                    }
//                    else{
//                        location.reload();
//                    }
//                    }
//                });
//
//    }
//    else{
//        return false;
//    }
//}


$.ajaxSetup({
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
             }

             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
         }
    });