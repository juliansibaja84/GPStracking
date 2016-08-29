setInterval(queryServer, 2000);
var map;

function initMap()
{
    map = new google.maps.Map(document.getElementById('map'), {
        center: new google.maps.LatLng(10.968840, -74.900124),
        zoom: 19,
    });
    // var marker = new google.maps.Marker({
    //     position: pos,
    //     map: map,
    //     title: 'Holi',
    // });
}

function queryServer()
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            comprehendInput(xhttp.responseText);
        }
    };
    xhttp.open("GET", "http://enomoto.sytes.net:5002/finder/req/one", true);
}

function comprehendInput(input)
{
    prett = JSON.parse(input);
    latitude  = prett.lat;
    longitude = prett.lon;
    time = prett.time;

    document.getElementById('long').innerHTML = longitude;
    document.getElementById('lati').innerHTML = latitude;
    document.getElementById('time').innerHTML = time;

}

function drawPoint(latitude, longitude, time)
{
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(latitude, longitude),
        map: map,
        title: time,
    });
    map.setCenter(new google.maps.LatLng(latitude, longitude));
}
