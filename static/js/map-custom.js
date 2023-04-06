(function($) {
    "use strict";
  
    $(document).ready(function() {
      const selector_map = $('#google_map');
      const { dataMapX: latitude = 51.526331228, dataMapY: longitude =  -0.470331452, dataPin: img_pin = 'images/icons/location.png', dataScrollwhell: scrollwhell = 0, dataDraggable: draggable = 0 } = selector_map.data();
      const style = [
        {
          "featureType": "administrative",
          "elementType": "all",
          "stylers": [
            {
              "saturation": "-100"
            }
          ]
        },
        {
          "featureType": "administrative.province",
          "elementType": "all",
          "stylers": []
        },
        {
          "featureType": "landscape",
          "elementType": "all",
          "stylers": [
            {
              "saturation": -100
            },
            {
              "lightness": 65
            },
            {
              "visibility": "on"
            }
          ]
        },
        {
          "featureType": "poi",
          "elementType": "all",
          "stylers": [
            {
              "saturation": -100
            },
            {
              "lightness": "50"
            },
            {
              "visibility": "simplified"
            }
          ]
        },
        {
          "featureType": "road",
          "elementType": "all",
          "stylers": [
            {
              "saturation": "-100"
            }
          ]
        },
        {
          "featureType": "road.highway",
          "elementType": "all",
          "stylers": []
        },
        {
          "featureType": "road.arterial",
          "elementType": "all",
          "stylers": []
        },
        {
          "featureType": "road.local",
          "elementType": "all",
          "stylers": []
        },
        {
          "featureType": "transit",
          "elementType": "all",
          "stylers": [
            {
              "saturation": -100
            },
            {
              "visibility": "simplified"
            }
          ]
        },
        {
          "featureType": "water",
          "elementType": "all",
          "stylers": [
            {
              "saturation": -100
            },
            {
              "lightness": "30"
            }
          ]
        }
      ];
  
      if (selector_map) {
        const map = new google.maps.Map(document.getElementById('google_map'), {
          zoom: 12,
          scrollwheel,
          navigationControl: true,
          mapTypeControl: false,
          scaleControl: false,
          draggable,
          styles: style,
          center: new google.maps.LatLng(latitude, longitude),
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });
  
        const infowindow = new google.maps.InfoWindow();
  
        let marker, i;
        const locations = [['Welcome', latitude, longitude, 2]];
        for (i = 0; i < locations.length; i++) {
          marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i][1], locations[i][2]),
            map,
            icon: img_pin
          });
  
          google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
              infowindow.setContent(locations[i][0]);
              infowindow.open(map, marker);
            }
          })(marker, i));
        }
      }
    });
  })(jQuery);
  