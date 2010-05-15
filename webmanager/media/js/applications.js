function changeState(){
    return toggle('app_filter');
}


function toggle(id) {
    var e = document.getElementById(id);
    if (e.style.display=="none") {
        e.style.display="block";
    } else {
        e.style.display="none";
    }
}
