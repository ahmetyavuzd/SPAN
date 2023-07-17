var map = L.map('map').setView([51.505, -0.09], 1);

var googleBasemap = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
    attribution:"SPAN Map View",
    maxZoom:22,
    subdomains:['mt0','mt1','mt2','mt3']
});
// var basemap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
googleBasemap.addTo(map);

function addMarker(latitude, longitude) {
  map.setView([latitude, longitude], 18);
  var marker_add = L.marker([latitude, longitude],{draggable:'false'}).addTo(map)
}

function addMarkerFrame2(latitude, longitude,message) {
  var marker_add2 = L.marker([latitude, longitude]).addTo(map)
  // marker_add2.bindPopup(message).openPopup();
  marker_add2.bindTooltip(message,{direction: 'top'}).openTooltip();

}

function addPoly(coordinates,center_lat,center_lon,color) {
  var latlng = JSON.parse(coordinates);
  map.setView([center_lat,center_lon], 21);
  var polygon = L.polygon(latlng, {color: color}).addTo(map);
}
