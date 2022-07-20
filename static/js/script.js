function required(){
    var empt = document.forms["Form"]["listNum"].value;
    if (empt == "")
    {
        alert("Please input number");
        return false;
    }
    return true; 
}

