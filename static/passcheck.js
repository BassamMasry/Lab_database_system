function alphanum(str) {
  var code, i, len;

  for (i = 0, len = str.length; i < len; i++) {
    code = str.charCodeAt(i);
    if (!(code > 47 && code < 58) && // numeric (0-9)
        !(code > 64 && code < 91) && // upper alpha (A-Z)
        !(code > 96 && code < 123) && // lower alpha (a-z)
        !(str[i] == '#' || str[i] == '$' || str[i] == '_')) {
      return false;
    }
  }
  return true;
};
function contain_num(str) {
  var code, i, len;

  for (i = 0, len = str.length; i < len; i++) {
    code = str.charCodeAt(i);
    if ((code > 47 && code < 58)) // numeric (0-9)
     {
         return true;
    }
  }
  return false;
};

function contain_alpha(str) {
  var code, i, len;

  for (i = 0, len = str.length; i < len; i++) {
    code = str.charCodeAt(i);
    if ((code > 64 && code < 91) || (code > 96 && code < 123)) // upper and lower alpha
     {
         return true;
    }
  }
  return false;
};

function contain_spec(str) {
  var i, len;
  for (i = 0, len = str.length; i < len; i++) {
    if ((str[i] == '#' || str[i] == '$' || str[i] == '_'))
     {
         return true;
    }
  }
  return false;
};

document.getElementById("form").onsubmit = function ()
{
    let input = document.getElementById("user_input");
    let password = document.getElementById("password");
    let confirm = document.getElementById("confirm");
    if(input.value != "")
    {
        $.get('/check?username=' + input.value, function(data) {
            if(data == true)
            {
                pass = alphanum(password.value) && contain_num(password.value) && contain_alpha(password.value) && contain_spec(password.value);
                if(pass)
                {
                    if(password.value == confirm.value)
                    {
                        document.getElementById("form").submit();
                        return true;
                    }
                    alert("password and confirmation do not match");
                    return false;
                }
                else if (!pass && !contain_num(password.value))
                {
                 alert("Must include at least one number");
                 return false;
                }
                else if (!pass && !contain_alpha(password.value))
                {
                 alert("Must include at least one letter");
                 return false;
                }
                else if (!pass && !contain_spec(password.value))
                {
                 alert("Must include at least # or $ or _");
                 return false;
                }
            }
            alert("Username not availible");
            return false;
        })
    }
    return false;
}