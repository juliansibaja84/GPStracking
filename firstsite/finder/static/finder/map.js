setInterval(queryServerOne, 2000);
var map;

function initMap()
{
    map = new google.maps.Map(document.getElementById('map'), {
        center: new google.maps.LatLng(10.968840, -74.900124),
        zoom: 19,
    });
    queryServerAll();
}

function queryServerAll()
{
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            comprehendInputa(xhttp.responseText);
        }
    };
    xhttp.open("GET", "http://localhost:8000/finder/req/all", true);
    xhttp.send();
}
// pay attention. En inputa tienes que hacer lo del drawPoint en un for
// lo de la tabla está raro

function queryServerOne()
{
    //
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            comprehendInput(xhttp.responseText);
        }
    };
    xhttp.open("GET", "http://localhost:8000/finder/req/one", true);
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
    drawPoint(latitude, longitude, tim);

}

function comprehendInputa(input)
{

    prett = JSON.parse(input);
    var thead = document.getElementById('tabla_suprema'); 
    var current = thead.innerHTML;
    var tnrow = ""; 
    var tdata = "";
    var lon = prett.lon.split(";"); 
    var lat = prett.lat.split(";");
    var prt = prett.prt.split(";");
    var ips = prett.ips.split(";");
    var tmp = prett.tmp.split(";");

    for(var j = 0; j<lon.length; ++j){

        tnrow="<td>"+lat[j]+"</td>"+"<td>"+lon[j]+"</td>"+"<td>"+tmp[j]+"</td>"+"<td>"+ips[j]+"</td>"+"<td>"+prt[j]+"</td>";
        tdata=tdata+"<tr>"+tnrow+"</tr>";
    }

    thead.innerHTML=current+tdata;

    for(var i=0;i<lon.length;++i){
        drawPoint(lat[i],lon[i],tmp[i]);
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
