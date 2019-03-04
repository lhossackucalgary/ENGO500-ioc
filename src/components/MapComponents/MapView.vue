<template>
    <div id="map"></div>
</template>

<script>
/* eslint-disable */
import Feature from 'ol/Feature.js';
import {Map as OLMap, View} from 'ol';
import Point from 'ol/geom/Point.js';
import Overlay from 'ol/Overlay.js';
import {Tile as TileLayer, Vector as VectorLayer} from 'ol/layer.js';
import {Vector as VectorSource} from 'ol/source.js';
import XYZ from 'ol/source/XYZ';
import {fromLonLat} from 'ol/proj';
import {Fill, Stroke, Style, Icon} from 'ol/style.js';

function getLocations(listOfThings, outputMap) {
  function getLocation(i) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = (function(id) {
      return function() {
        if (this.readyState == 4 && this.status == 200) {
          var responseJSON = JSON.parse(xhttp.responseText);
          if (responseJSON['@iot.count'] > 0) {
            outputMap.set(id, responseJSON.value[0].location.coordinates);
          } else {
            // Remove thing id from list of things if it doesn't have a location..
            var index = listOfThings.indexOf(id);
            if (index > -1) {
              listOfThings.splice(index, 1);
            }
          }
        }
      }
    })(listOfThings[i]);

    xhttp.open("GET", "http://routescout.sensorup.com/v1.0/Things(" + listOfThings[i] + ")/Locations", true);
    xhttp.send();
  }

  for (var i = 0; i < listOfThings.length; i++) {
    getLocation(i);
  }
}

function getThings(things_props, thing_id_list, things_locations_map) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var things_list = JSON.parse(xhttp.responseText).value;
      for (var t = 0; t < things_list.length; t++) {
        thing_id_list.push(things_list[t]['@iot.id']);
        things_props.set(things_list[t]['@iot.id'], things_list[t]);
      }
      getLocations(thing_id_list, things_locations_map);
    }
  };
  xhttp.open("GET", "http://routescout.sensorup.com/v1.0/Things", true);
  xhttp.send();
}


function LoadMapData(things, thing_ids, thing_locations, vecSource, vecLayer) {
  things.clear();
  thing_ids.length = 0;
  thing_locations.clear();
  getThings(things, thing_ids, thing_locations);

  // crewLocations will be filled async by getLocations..
  var intervalId = setInterval(function() {
    if (thing_ids.length > 0 && thing_locations.size == thing_ids.length) {
      // Add data into layer groups

      for (let i = 0; i < thing_ids.length; i++) {
        let feature_s = new Feature(new Point(fromLonLat(thing_locations.get(thing_ids[i]))));
        feature_s.setProperties({"name": "myName", "desc": "descriptino"});
        vecSource.addFeature(feature_s);
      }

      clearInterval(intervalId);
      return;
    }
  }, 250);
}

var vectorSource = new VectorSource();

var iconStyle = new Style({
  image: new Icon(/** @type {module:ol/style/Icon~Options} */ ({
    anchor: [0.5, 50],
    anchorXUnits: 'fraction',
    anchorYUnits: 'pixels',
    src: require('../../assets/logo.png'),
    scale: 0.1
  }))
});


var vectorLayer = new VectorLayer({
  source: vectorSource,
  style: iconStyle
});

export default {
  mounted () {
    var M = new OLMap({
      target: 'map',
      layers: [
        new TileLayer({
          source: new XYZ({
            url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'
          })
        }),
        vectorLayer
      ],
      view: new View({
        center: fromLonLat([-114,51]),
        zoom: 10
      })
    });

    var thing_locations = new Map();  //map crew id to location
    var things = new Map(); //map crew id to props
    var thing_ids = [];



    LoadMapData(things, thing_ids, thing_locations, vectorSource, vectorLayer);
    var dataLoader = setInterval(function() {
      LoadMapData(things, thing_ids, thing_locations, vectorSource, vectorLayer);
    }, 60000); // 60000 == 1 minute

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("https://openlayers.org/en/latest/css/ol.css")

#map {
  position: fixed;
  bottom: 0;
  right: 0;
}
</style>
