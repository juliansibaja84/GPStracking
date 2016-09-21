var map;
var polyline;
var old_marker = null;
var cur_input = "";
var poly_pos = [];
var location_lat;
var location_lng;
var markers = [];
var markers_area = [];
var markerus = [];
var area_status = false;
var rectangle;

function initMap()
{
    map = new google.maps.Map(document.getElementById('map'), {
        center: new google.maps.LatLng(10.968840, -74.900124),
        zoom: 12,
    });
    google.maps.event.addListener(map, 'rightclick', function(event) {
        if(area_status == false) {
            location_lat = event.latLng.lat();
            location_lng = event.latLng.lng();
            if(markeru != []){
               deleteMarkers(markerus); 
            }
            var markeru = new google.maps.Marker({
                position: new google.maps.LatLng(location_lat, location_lng),
                map: map,
                title: "lat:"+location_lat+"  lon: "+location_lng,
                icon: '/static/finder/markera_temp.png',
            });
            markerus.push(markeru);
            drawRectangles();
            area_status = true;
            document.getElementById('info_panel').innerHTML = 'Vuelve a hacer <span>click</span> derecho en el mapa para eliminar la selección de coordenadas actual';
        }
        else {
            deleteMarkers(markerus);
            rectangle.setMap(null);
            area_status = false;
            document.getElementById('info_panel').innerHTML = 'Puede Hacer <span>click</span> derecho en el mapa para mostrar coordenadas en ese punto del mapa';
        }
    });
    polyline = new google.maps.Polyline({
        map: map,
        path: poly_pos,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
}

function drawRectangles()
{
    rectangle = new google.maps.Rectangle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: map,
        bounds: {
        north: location_lat + 0.0032,
        south: location_lat - 0.0032,
        east: location_lng + 0.0032,
        west: location_lng - 0.0032
        }
    });
}

function getDateInterval()
{
    var lower = document.getElementById('lower_lim').value;
    var upper = document.getElementById('upper_lim').value;
    if(lower > upper || lower == "" || upper == "") {
        alert("Por favor ingrese una combinación de fechas válida");
    }
    else {
        lower += ":00";
        upper += ":00";
        if(area_status == true)
            queryServerR(lower, upper);
        else
            queryServerAll(lower, upper)
    }
    return false;
}

function queryServerAll(lower, upper)
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

function comprehendInputAll(input)
{
    prett = JSON.parse(input);
    var lon = prett.lon.split(";"); 
    var lat = prett.lat.split(";");
    var prt = prett.prt.split(";");
    var ips = prett.ips.split(";");
    var tmp = prett.tmp.split(";");

    document.getElementById("cant").innerHTML = "Se encontraron " + tmp.length + " resultados que satisfacen sus criterios de búsqueda";

    polypos = [];
    for(var i=0;i<lon.length;++i){
        cur_input = tmp[i];
        drawPoint(lat[i],lon[i],tmp[i]);
    }
}

function drawPoint(latitude, longitude, time)
{
    poly_pos.push({lat: parseFloat(latitude),lng: parseFloat(longitude)});
    deleteMarkers(markerus);
    deleteMarkers(markers_area);
    polyline.setPath(poly_pos);
    polyline.setMap(map);
    if(old_marker != null)
        old_marker.setIcon('/static/finder/marker.png');
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(latitude, longitude),
        map: map,
        title: time,
        icon: '/static/finder/markera.png',
    });
    map.setCenter(new google.maps.LatLng(latitude, longitude));
    old_marker = marker;
    markers.push(marker);
}

function placeMarker(latitude,longitude,time) {
    var markerx = new google.maps.Marker({
        position: new google.maps.LatLng(latitude, longitude),
        map: map,
        title: time,
        icon: '/static/finder/markera.png',
    });
    markers_area.push(markerx);
}

function queryServerR(lower, upper){
    var rhttp = new XMLHttpRequest();
    rhttp.onreadystatechange = function() {
        if (rhttp.readyState == 4 && rhttp.status == 200) {
            if(JSON.parse(rhttp.response).lon != ''){
                for (var i = 0; i < markers.length; i++) {
                    markers[i].setMap(null);
                }
                markers = [];
            }
            recieveAndPutMkr(rhttp.responseText);

        }
    };
    rhttp.open("GET", "rq/"+location_lat+"/"+location_lng+"/"+lower+"/"+upper, true);
    rhttp.send();
}

function recieveAndPutMkr(input){
    var recieved = JSON.parse(input);
    var longit = recieved.lon.split(";"); 
    var latit = recieved.lat.split(";");
    var tiempo = recieved.tmp.split(";");

    deleteMarkers(markerus);
    deleteMarkers(markers_area);
    deleteMarkers(markers);

    polyline.setMap(null);
    for(var i=0;i<longit.length;++i){
        placeMarker(latit[i],longit[i],tiempo[i]);
    }
    document.getElementById("cant").innerHTML = "Se encontraron " + tiempo.length + " resultados que satisfacen sus criterios de búsqueda";
}

function deleteMarkers(marki){
    for (var i = 0; i < marki.length; i++) {
        marki[i].setMap(null);
    }
    marki = [];
}
