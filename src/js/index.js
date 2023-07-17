var map = L.map('map').setView([51.505, -0.09], 1);

var googleBasemap = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', {
    attribution:"SPAN Map View",
    maxZoom:22,
    subdomains:['mt0','mt1','mt2','mt3']
});
// var basemap = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
googleBasemap.addTo(map);
var marker = null;
var geocoder = L.Control.geocoder({
    defaultMarkGeocode: true,
    position:"topleft"
  })
    // .on('markgeocode', function(e) {
    //   var bbox = e.geocode.bbox;
    //   var poly = L.polygon([
    //     bbox.getSouthEast(),
    //     bbox.getNorthEast(),
    //     bbox.getNorthWest(),
    //     bbox.getSouthWest()
    //   ]).addTo(map);
    //   map.fitBounds(poly.getBounds());
    // })
    // .addTo(map);
  
  geocoder.addTo(map);

// var locationIcon = L.icon ({
//   iconUrl: 'C:\\Users\\ahmet\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\python\\plugins\\solar_pw_calculator\\locationIcon.png',
//   iconSize: [48,48],
//   iconAnchor: [22,40]
// })

map.on('click', function (e) {
    if (marker !== null) {
        map.removeLayer(marker);
    }
    var coord = e.latlng;
    var lat = coord.lat;
    var lng = coord.lng;
    
    console.log(lat + "," + lng);
    marker = L.marker(e.latlng,{draggable:'true'}).addTo(map)
});

function addMarker(latitude, longitude) {
  map.setView([latitude, longitude], 18);
  var marker_add = L.marker([latitude, longitude],{draggable:'true'}).addTo(map)
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

// addPoly([[39,40],[40,40],[40,41],[41,41]])
