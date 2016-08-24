//var map;
//var pos = {lat: +10.98995, lng: -74.82617};
//function initMap() {
//    map = new google.maps.Map(document.getElementById('map'), {
//        center: pos,
//        zoom: 19,
//    });
//    var marker = new google.maps.Marker({
//        position: pos,
//        map: map,
//        title: 'Holi',
//    });
//}
setInterval(queryServer, 2000);

function queryServer()
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            //window.alert(xhttp.responseText);
        }
    };
    xhttp.open("GET", "http://127.0.0.1:8000/finder/req", true);
    xhttp.send();
}