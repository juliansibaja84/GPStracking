var map;
var pos = {lat: +10.98995, lng: -74.82617};
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: pos,
        zoom: 19,
    });
    var marker = new google.maps.Marker({
        position: pos,
        map: map,
        title: 'Holi',
    });
}