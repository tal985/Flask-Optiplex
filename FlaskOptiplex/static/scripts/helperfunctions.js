/* Client-Side JavaScript Validation */

function validCheck()
{
    var ip = document.getElementsByName("ip")[0].value;
    var port = document.getElementsByName("port")[0].value;

    if (validIP(ip) && validPort(port))
        return true;

    return false;
}

function validIP(input) 
{
    var ip = input.split(".");

    if (ip.length != 4)
        return false;

    if (ip[0] == '192' || ip[0] == '10' || ip[0] == '010')
        return false;

    for (i = 0; i < ip.length; i++)
    {
        if (ip[i] == "")
            return false;
        temp = parseInt(ip[i]);
        if (temp > 255 || temp < 0)
            return false;
    }

    return true;
}

function validPort(input)
{
    if (input > 0 && input <= 65535)
        return true;
    return false;
}
