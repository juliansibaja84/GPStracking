var map;
var polyline;
var old_marker;
var cur_input = "";
var poly_pos = [];

function initMap()
{
    map = new google.maps.Map(document.getElementById('map'), {
        center: new google.maps.LatLng(10.968840, -74.900124),
        zoom: 19,
    });
    
    old_marker = new google.maps.Marker({
        position: new google.maps.LatLng(0, 0),
        map: map,
    });
    setInterval(queryServerOne, 2000);

}

function queryServerOne()
{
    //
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            comprehendInput(xhttp.responseText);
        }
    };
    xhttp.open("GET", "req/one", true);
    xhttp.send();
}

function comprehendInput(input)
{
    prett = JSON.parse(input);
    latitude  = prett.lat;
    longitude = prett.lon;
    tim = prett.tmp;

    document.getElementById('long').innerHTML = longitude;
    document.getElementById('lati').innerHTML = latitude;
    document.getElementById('time').innerHTML = tim;

    if(cur_input != prett.tmp) {
        cur_input = prett.tmp;
        var thead = document.getElementById('tabla_suprema');
        drawPoint(latitude, longitude, tim);
    }

}

function drawPoint(latitude, longitude, time)
{
    //determine_poly_set(time)
    poly_pos.push({lat: parseFloat(latitude),lng: parseFloat(longitude)});
    
    polyline = new google.maps.Polyline({
        path: poly_pos,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    
    polyline.setMap(map);

    old_marker.setIcon('/static/finder/marker.png');
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(latitude, longitude),
        map: map,
        title: time,
        icon: '/static/finder/markera.png',
    });
    map.setCenter(new google.maps.LatLng(latitude, longitude));
    old_marker = marker;
}