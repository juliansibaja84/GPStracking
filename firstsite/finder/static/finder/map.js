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
    xhttp.send();
    var xhttpa = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttpa.readyState == 4 && xhttpa.status == 200) {
            comprehendInputa(xhttpa.responseText);
        }
    };
    xhttpa.open("GET", "http://enomoto.sytes.net:5002/finder/req/all", true);
    xhttpa.send();
}

function comprehendInput(input)
{
    prett = JSON.parse(input);
    latitude  = prett.lat;
    longitude = prett.lon;
    time = prett.tmp;

    document.getElementById('long').innerHTML = longitude;
    document.getElementById('lati').innerHTML = latitude;
    document.getElementById('time').innerHTML = time;

}

function comprehendInputa(input)
{
    prett = JSON.parse(input);
    var thead = document.getElementById('theading');
    var current = thead.innerHTML;
    var tnrow = "";
    var tdata = "";
    var lon = prett.lon.split(";");
    var lat = prett.lat.split(";");
    var prt = prett.prt.split(";");
    var ips = prett.ips.split(";");
    var tmp = prett.tmp.split(";");

    for(var j = 0; j<lon.length; ++j){

        tnrow="<td>"+lat[j]+"</td>"+"<td>"+lon[j]+"</td>"+"<td>"+ip[j]+"</td>"+"<td>"+tmp[j]+"</td>"+"<td>"+prt[j]+"</td>";
        tdata=tdata+"<tr>"+tnrow+"</tr>";
    
    }

    thead.innerHTML=thead.innerHTML+tdata;
    
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
