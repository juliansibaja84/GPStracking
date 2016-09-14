var map;
var polyline;
var old_marker;
var cur_input = "";
var lower = "";
var upper = "";
var poly_pos = [];
var location_lat;
var location_lat;

function initMap()
{
    map = new google.maps.Map(document.getElementById('map'), {
        center: new google.maps.LatLng(10.968840, -74.900124),
        zoom: 12,
    });
    old_marker = new google.maps.Marker({
        position: new google.maps.LatLng(0, 0),
        map: map,
    });
    google.maps.event.addListener(map, 'click', function(event) {
        location_lat = event.latLng.lat();
        location_lng = event.latLng.lng();
        queryServerR(location_lat, location_lng);
        window.alert(location_lat+location_lng);
    });

}

function getDateInterval()
{
    lower = document.getElementById('lower_lim').value;
    upper = document.getElementById('upper_lim').value;
    lower += ":00";
    upper += ":00";
    alert(lower);
    if(lower > upper) {
        alert("Por favor ingrese una combinación de fechas válida");
    }
    else {
        queryServerAll()
    }
    return false;
}

function queryServerAll()
{
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            comprehendInputAll(xhttp.responseText);
        }
    };
    xhttp.open("GET", "req/"+lower+"/"+upper, true);
    xhttp.send();
}
// pay attention. En inputa tienes que hacer lo del drawPoint en un for
// lo de la tabla está raro

function comprehendInputAll(input)
{

    prett = JSON.parse(input);

    var lon = prett.lon.split(";"); 
    var lat = prett.lat.split(";");
    var prt = prett.prt.split(";");
    var ips = prett.ips.split(";");
    var tmp = prett.tmp.split(";");

    polypos = [];
    for(var i=0;i<lon.length;++i){
        cur_input = tmp[i];
        drawPoint(lat[i],lon[i],tmp[i]);
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

function placeMarker(latitude,longitude,time) {
    var markerx = new google.maps.Marker({
        position: new google.maps.LatLng(latitude, longitude),
        map: map,
        title: time,
        icon: '/static/finder/markera.png',
    });
}


function queryServerR(latit, longit){

    lower = document.getElementById('lower_lim').value;
    upper = document.getElementById('upper_lim').value;
    if(lower > upper) {
        alert("Por favor ingrese una combinación de fechas válida");
    }
    else {
        var rhttp = new XMLHttpRequest();
        rhttp.onreadystatechange = function() {
            if (rhttp.readyState == 4 && rhttp.status == 200) {
                recieveAndPutMkr(rhttp.responseText);
            }
        };
        rhttp.open("GET", "req/"+latit+"/"+longit+"/"+lower+"/"+upper, true);
        rhttp.send();
    }
    return false;      
}

function recieveAndPutMkr(input){

    var recieved = JSON.parse(input);
    var longit = recieved.lon.split(";"); 
    var latit = recieved.lat.split(";");
    var tiempo = recieved.tmp.split(";");

    for(var i=0;i<longit.length;++i){
        placeMarker(latit[i],longit[i],tiempo[i]);
    }

}