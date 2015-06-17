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

        if ( document.login_form.login.value == "" )
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