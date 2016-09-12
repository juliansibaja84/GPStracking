var map;
var polyline;
var old_marker;
var cur_input = "";
var lower = "";
var upper = "";
var poly_pos = [];
var locationll;
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
}

$('#contactForm').submit(function () {
    getDateInterval();
    return false;
});



function getDateInterval()
{
    lower = document.getElementById('lower_lim').value;
    upper = document.getElementById('upper_lim').value;
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
    //Obtener latitud y longitud con un click-------------------
    var infowindow = new google.maps.InfoWindow({
        content: "latitude: "+latitude+"  longitude: "+longitude
    });

    marker.addListener('click', function() {
        infowindow.open(marker.get('map'), marker);
        
    });
    //----------------------------------------------------------
    map.setCenter(new google.maps.LatLng(latitude, longitude));
    old_marker = marker;

}