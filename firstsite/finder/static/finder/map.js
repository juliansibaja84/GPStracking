var map;
var polyline;
var old_marker;
var old_marker_aux;
var cur_input = "";
var cur_input_aux = "";
var poly_pos = [];
var poly_pos_aux = [];
var truck = 'truck1';
var truck_last = 'truck1';
var id;
var id_aux;
var OBD_id = 0;

id_aux = setInterval(queryOBDData, 4000);

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

    id = setInterval(queryServerOne, 4000);

}

function queryOBDData()
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            fillOBDData(xhttp.responseText);
        }
    };
    if (OBD_id != 0) {
        xhttp.open("GET", "obd/" + truck + "/" + OBD_id, true);
        xhttp.send();
    }
}

function fillOBDData(response)
{
    var resp = JSON.parse(response);
    var obd_info1 = document.getElementById("span_data1");
    var obd_info2 = document.getElementById("span_data2");

    obd_info1.innerHTML = resp.val1;
    obd_info2.innerHTML = resp.val2;
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
    if (truck == "truck1"){
        xhttp.open("GET", "req/one", true);
        xhttp.send();
    }else if (truck == "truck2") {
        xhttp.open("GET", "req/oneanother", true);
        xhttp.send();
    }else if (truck == "truckb") {
        xhttp.open("GET", "req/many", true);
        xhttp.send();
    }
}

function comprehendInput(input)
{

    prett = JSON.parse(input);

    if(truck != "truckb") {
        latitude  = prett.lat;
        longitude = prett.lon;
        tim = prett.tmp;

        document.getElementById('long').innerHTML = " " + longitude;
        document.getElementById('lati').innerHTML = " " + latitude;
        document.getElementById('time').innerHTML = " " + tim;
        if (truck == truck_last){
            if(cur_input != prett.tmp) {
                cur_input = prett.tmp;
                drawPoint(latitude, longitude, tim, truck);
            }
        }else{
            drawPoint(latitude, longitude, tim, truck);
            truck_last = truck;
            cur_input = "";
        }
    }else {
        lat1 = prett.lat1;
        lon1 = prett.lon1;
        tim1 = prett.tmp1;

        lat2 = prett.lat2;
        lon2 = prett.lon2;
        tim2 = prett.tmp2;

        document.getElementById('long').innerHTML = " " + lon1 + "  " + lon2;
        document.getElementById('lati').innerHTML = " " + lat1 + "  " + lat2;
        document.getElementById('time').innerHTML = " " + tim1 + "  " + tim2;
        if (cur_input != tim1) {
            cur_input = tim1;
            drawPoint(lat1, lon1, tim1, 'truck1');
        }
        if (cur_input_aux != tim2) {
            cur_input_aux = tim2;
            drawPointAux(lat2, lon2, tim2);
        }
    }
}

function drawPointAux(latitude, longitude, time)
{
    //determine_poly_set(time)
    poly_pos_aux.push({lat: parseFloat(latitude),lng: parseFloat(longitude)});
    var colorin = '#017f18';
    polyline = new google.maps.Polyline({
        path: poly_pos_aux,
        geodesic: true,
        strokeColor: colorin,
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    
    polyline.setMap(map);

    if (old_marker_aux != undefined){
        old_marker_aux.setIcon('/static/finder/markerAnother.png');
    }

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(latitude, longitude),
        map: map,
        title: time,
        icon: '/static/finder/markeraAnother.png',
    });

    map.setCenter(new google.maps.LatLng(latitude, longitude));
    old_marker_aux = marker;
}

function drawPoint(latitude, longitude, time, trk)
{
    //determine_poly_set(time)
    poly_pos.push({lat: parseFloat(latitude),lng: parseFloat(longitude)});
    var colorin = '#FF0000';
    if (trk == 'truck2') {
        colorin = '#017f18';
    }
    polyline = new google.maps.Polyline({
        path: poly_pos,
        geodesic: true,
        strokeColor: colorin,
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    
    polyline.setMap(map);

    if (trk == "truck1"){
        if (old_marker != undefined){
            old_marker.setIcon('/static/finder/marker.png');
        }
    
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(latitude, longitude),
            map: map,
            title: time,
            icon: '/static/finder/markera.png',
        });
    }else if (trk == "truck2"){
        if (old_marker != undefined){
            old_marker.setIcon('/static/finder/markerAnother.png');
        }
    
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(latitude, longitude),
            map: map,
            title: time,
            icon: '/static/finder/markeraAnother.png',
        });
    }

    map.setCenter(new google.maps.LatLng(latitude, longitude));
    old_marker = marker;
}

function getTruck(){
    var e = document.getElementById("truck");
    truck = e.options[e.selectedIndex].value;
    old_marker = null;
    poly_pos = [];
    poly_pos_aux = [];
    cur_input = "";
    cur_input_aux = "";
    polyline.setPath(poly_pos);
    clearInterval(id);
    initMap();
}

function changeOBDMeasure()
{
    var e = document.getElementById("obd_measure");
    var obd_info1_g = document.getElementById("data1");
    var obd_info2_g = document.getElementById("data2");
    var obd_info1 = document.getElementById("span_data1");
    var obd_info2 = document.getElementById("span_data2");

    var i = e.options[e.selectedIndex].value;
    switch(i) {
        case '0':
            OBD_id = 0;
            obd_info1_g.innerHTML = 'You are not measuring any data from your vehicle. <span id="span_data1"></span>';
            obd_info2_g.innerHTML = '<span id="span_data2"></span>';
            break;
        case '1':
            OBD_id = 1;
            obd_info1_g.innerHTML = 'Trouble codes: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Trouble codes: <span id="span_data2"></span>';
            break;
        case '2':
            OBD_id = 2;
            obd_info1_g.innerHTML = 'Engine RPM: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Engine RPM: <span id="span_data2"></span>';
            break;
        case '3':
            OBD_id = 3;
            obd_info1_g.innerHTML = 'Engine load: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Engine load: <span id="span_data2"></span>';
            break;
        case '4':
            OBD_id = 4;
            obd_info1_g.innerHTML = 'Fuel pressure: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Fuel pressure: <span id="span_data2"></span>';
            break;
        case '5':
            OBD_id = 5;
            obd_info1_g.innerHTML = 'Vehicle speed: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Vehicle speed: <span id="span_data2"></span>';
            break;
        case '6':
            OBD_id = 6;
            obd_info1_g.innerHTML = 'Throttle position: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Throttle position: <span id="span_data2"></span>';
            break;
        case '7':
            OBD_id = 7;
            obd_info1_g.innerHTML = 'Time since engine start: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Time since engine start: <span id="span_data2"></span>';
            break;
        case '8':
            OBD_id = 8;
            obd_info1_g.innerHTML = 'Distance traveled: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Distance traveled: <span id="span_data2"></span>';
            break;
        case '9':
            OBD_id = 9;
            obd_info1_g.innerHTML = 'Battery voltage: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Battery voltage: <span id="span_data2"></span>';
            break;
    }
}