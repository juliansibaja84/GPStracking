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
    xhttp.open("GET", "finder/req/all", true);
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
    xhttp.open("GET", "finder/req/one", true);
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
        var tnrow = "<td>"+latitude+"</td>"+"<td>"+longitude+"</td>"+"<td>"+tim+"</td>"+"<td>"+prett.ips+"</td>"+"<td>"+prett.prt+"</td>";
        thead.innerHTML = thead.innerHTML + "<tr>" + tnrow + "</tr>";
        drawPoint(latitude, longitude, tim);
    }

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
        cur_input = tmp[i];
        drawPoint(lat[i],lon[i],tmp[i]);
    }
    setInterval(queryServerOne, 2000);
}

function drawPoint(latitude, longitude, time)
{
    //determine_poly_set(time)
    poly_pos.push({lat: parseFloat(latitude),lng: parseFloat(longitude)});
    //window.alert(poly_pos);
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