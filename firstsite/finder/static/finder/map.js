var map;
var polyline;
var old_marker;
var cur_input = "";
var poly_pos = [];
var truck = 'truck1';
var truck_last = 'truck1';

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
    if (truck == "truck1"){
        xhttp.open("GET", "req/one", true);
        xhttp.send();
    }else if (truck == "truck2") {
        xhttp.open("GET", "req/oneanother", true);
        xhttp.send();
    }
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
    if (truck == truck_last){
        if(cur_input != prett.tmp) {
            cur_input = prett.tmp;
            drawPoint(latitude, longitude, tim);
        }
    }else{
        drawPoint(latitude, longitude, tim);
        truck_last = truck;
        cur_input = "";
    }

}

function drawPoint(latitude, longitude, time)
{
    //determine_poly_set(time)
    poly_pos.push({lat: parseFloat(latitude),lng: parseFloat(longitude)});
    var colorin = '#FF0000'
    if (truck == 'truck2')
        colorin = '#017f18';
    polyline = new google.maps.Polyline({
        path: poly_pos,
        geodesic: true,
        strokeColor: colorin,
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    
    polyline.setMap(map);
    if (truck == "truck1"){
        if (old_marker != undefined){
            old_marker.setIcon('/static/finder/marker.png');
        }
    
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(latitude, longitude),
            map: map,
            title: time,
            icon: '/static/finder/markera.png',
        });
    }else if (truck == "truck2"){
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
    polyline.setPath(poly_pos);
    initMap();
}

function changeOBDMeasure()
{
    var e = document.getElementById("obd_measure");
    var obd_info1_g = document.getElementById("data1");
    var obd_info2_g = document.getElementById("data2");
    var obd_info1 = document.getElementById("span_data1");
    var obd_info2 = document.getElementById("span_data2");

    truck = e.options[e.selectedIndex].value;
    switch(truck) {
        case '0':
            obd_info1_g.innerHTML = 'You are not measuring any data from your vehicle. <span id="span_data1"></span>';
            obd_info2_g.innerHTML = '<span id="span_data2"></span>';
            break;
        case '1':
            obd_info1_g.innerHTML = 'Trouble codes: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Trouble codes: <span id="span_data2"></span>';
            break;
        case '2':
            obd_info1_g.innerHTML = 'Engine RPM: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Engine RPM: <span id="span_data2"></span>';
            break;
        case '3':
            obd_info1_g.innerHTML = 'Engine load: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Engine load: <span id="span_data2"></span>';
            break;
        case '4':
            obd_info1_g.innerHTML = 'Fuel pressure: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Fuel pressure: <span id="span_data2"></span>';
            break;
        case '5':
            obd_info1_g.innerHTML = 'Vehicle speed: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Vehicle speed: <span id="span_data2"></span>';
            break;
        case '6':
            obd_info1_g.innerHTML = 'Throttle position: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Throttle position: <span id="span_data2"></span>';
            break;
        case '7':
            obd_info1_g.innerHTML = 'Time since engine start: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Time since engine start: <span id="span_data2"></span>';
            break;
        case '8':
            obd_info1_g.innerHTML = 'Distance traveled: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Distance traveled: <span id="span_data2"></span>';
            break;
        case '9':
            obd_info1_g.innerHTML = 'Battery voltage: <span id="span_data1"></span>';
            obd_info2_g.innerHTML = 'Battery voltage: <span id="span_data2"></span>';
            break;
    }
}