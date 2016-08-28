setInterval(queryServer, 2000);

var map;
var marked = [{lat: 1, lng: 2}];

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
    xhttp.open("GET", "/finder/req", true);
    xhttp.send();
}

function comprehendInput(input)
{
    prett = JSON.parse(input);
    latitude  = prett.lat;
    longitude = prett.lon;
    time = prett.time;

    var check = 1;
    for(var i = 0; i < marked.length; ++i) {
        if(marked[i].lat == latitude && marked[i].lon == longitude)
            check = 0;
    }
    if(check == 1) {
        marked.push(prett);
        drawPoint(latitude, longitude, time);
    }
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