var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: +10.98995, lng: -74.82617},
        zoom: 8
    });
}