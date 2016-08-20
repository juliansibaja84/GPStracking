var map;
    function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
        center: new google.maps.LatLng(+10.98995, -74.82617),
        zoom: 1,
    });
window.eqfeed_callback = function(results) {
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(10.98995, -74.82617),
        map: map
        });
    }
}

