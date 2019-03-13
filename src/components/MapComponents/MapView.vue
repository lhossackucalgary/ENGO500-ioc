<template>
  <div class="">
    <div id="map"></div>
    <!--div id="popup">STUFF</div-->
    <div id="popup"></div>
  </div>
</template>

<script>
/* eslint-disable */
import Feature from 'ol/Feature.js';
import {Map as OLMap, View} from 'ol';
import Point from 'ol/geom/Point.js';
import LineString from 'ol/geom/LineString';
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


function LoadMapData(things, thing_ids, thing_locations, b_healthy_src, b_warning_src,
                     b_urgent_src, b_unknown_src, b_needsparts_src, c_src, route_src) {
  things.clear();
  thing_ids.length = 0;
  thing_locations.clear();
  getThings(things, thing_ids, thing_locations);

  function data_load_check() {
    if (thing_ids.length > 0 && thing_locations.size == thing_ids.length) {
      //console.log(things);
      //console.log(thing_locations);

      b_healthy_src.clear();
      b_warning_src.clear();
      b_urgent_src.clear();
      b_unknown_src.clear();
      b_needsparts_src.clear();
      c_src.clear();
      route_src.clear();

      for (let i = 0; i < thing_ids.length; i++) {
        // Create feature
        let feature_s = new Feature(new Point(fromLonLat(thing_locations.get(thing_ids[i]))));
        var thing_ = things.get(thing_ids[i]);
        feature_s.setProperties(thing_);
        var props_ = thing_["properties"];

        // Assign to a layer source
        if (typeof(props_["status"]) !== "undefined") {
          // is a robot
          if (props_["status"] === "Healthy") {
            b_healthy_src.addFeature(feature_s);
          } else if (props_["status"] === "Warning") {
            b_warning_src.addFeature(feature_s);
          } else if (props_["status"] === "SICK AF") {
            b_urgent_src.addFeature(feature_s);
          } else if (props_["status"] === "Unknown") {
            b_unknown_src.addFeature(feature_s);
          } else if (props_["status"] === "Needs parts") {
            b_needsparts_src.addFeature(feature_s);
          }
        }
        if (typeof(props_["route"]) !== "undefined") { //(thing_["properties"]["route"] !== "undefined") {
          // is a crew
          c_src.addFeature(feature_s);
          // also print their route to a layer..

          if (props_["route"].length >= 1) {
            // Add crew's location
            var list_of_coords = [fromLonLat(thing_locations.get(thing_ids[i]))];

            // Add location of each bot:
            for (let i = 0; i < props_["route"].length; i++) {
              list_of_coords.push(fromLonLat(thing_locations.get(props_["route"][i])));
            }
            var route_feature = new Feature(new LineString(list_of_coords));
            route_src.addFeature(route_feature);
          }
        }

        /*        if is bot (true) {
        } else if is crew (true) {
        }*/

      }
      return;
    } else {
      setTimeout(data_load_check, 500);
    }
  }

  data_load_check();
}

// var vectorSource = new VectorSource();
var bots_healthy_source = new VectorSource();
var bots_warning_source = new VectorSource();
var bots_urgent_source = new VectorSource();
var bots_unknown_source = new VectorSource();
var bots_needsparts_source = new VectorSource();
var crews_source = new VectorSource();
var routes_source = new VectorSource();

var bots_healthy_layer = new VectorLayer({
  source: bots_healthy_source,
  style: new Style({
    image: new Icon(/** @type {module:ol/style/Icon~Options} */ ({
      anchor: [0.5, 0.5],
      anchorXUnits: 'fraction',
      anchorYUnits: 'fraction',
      src: require('../../assets/Healthy.png'),
      scale: 0.7
    }))
  })
});
var bots_warning_layer = new VectorLayer({
  source: bots_warning_source,
  style: new Style({
    image: new Icon(/** @type {module:ol/style/Icon~Options} */ ({
      anchor: [0.5, 0.5],
      anchorXUnits: 'fraction',
      anchorYUnits: 'fraction',
      src: require('../../assets/Warning.png'),
      scale: 0.7
    }))
  })
});
var bots_urgent_layer = new VectorLayer({
  source: bots_urgent_source,
  style: new Style({
    image: new Icon(/** @type {module:ol/style/Icon~Options} */ ({
      anchor: [0.5, 0.5],
      anchorXUnits: 'fraction',
      anchorYUnits: 'fraction',
      src: require('../../assets/Urgent.png'),
      scale: 0.7
    }))
  })
});
var bots_unknown_layer = new VectorLayer({
  source: bots_unknown_source,
  style: new Style({
    image: new Icon(/** @type {module:ol/style/Icon~Options} */ ({
      anchor: [0.5, 0.5],
      anchorXUnits: 'fraction',
      anchorYUnits: 'fraction',
      src: require('../../assets/Unknown.png'),
      scale: 0.7
    }))
  })
});
var bots_needsparts_layer = new VectorLayer({
  source: bots_needsparts_source,
  style: new Style({
    image: new Icon(/** @type {module:ol/style/Icon~Options} */ ({
      anchor: [0.5, 0.5],
      anchorXUnits: 'fraction',
      anchorYUnits: 'fraction',
      src: require('../../assets/NeedsParts.png'),
      scale: 0.7
    }))
  })
});
var crews_layer = new VectorLayer({
  source: crews_source,
  style: new Style({
    image: new Icon(/** @type {module:ol/style/Icon~Options} */ ({
      anchor: [0.5, 0.5],
      anchorXUnits: 'fraction',
      anchorYUnits: 'fraction',
      src: require('../../assets/Crew.png'),
      scale: 0.7
    }))
  })
});
var routes_layer = new VectorLayer({
  source: routes_source,
  style: new Style({
    stroke: new Stroke({
      color: 'green',
      width: 3
    })
  })
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
        bots_healthy_layer,
        bots_warning_layer,
        bots_urgent_layer,
        bots_unknown_layer,
        bots_needsparts_layer,
        crews_layer,
        routes_layer
      ],
      view: new View({
        center: fromLonLat([-114,51]),
        zoom: 10
      })
    });

    var popup = new Overlay({
      positioning: 'center-center',
      element: document.getElementById('popup'),
      autoPan: true,
      autoPanAnimation: {
        duration: 250
      },
      offset: [0, -60]
    });

    M.on('click', function (evt) {
      var hit = false;
      var obj = M.forEachFeatureAtPixel(evt.pixel, function (feature, layer) {
          hit = true;
          var popupStr = "";
          // Build popup string:
          if(typeof(feature["values_"]["properties"]["status"]) !== "undefined"){
            // Robot
            popupStr += "Name: " + feature["values_"]["name"];
            popupStr += "<br\>IotId: " + feature["values_"]["@iot.id"];
            popupStr += "<br\>Status: " + feature["values_"]["properties"]["status"];

            popup.getElement().innerHTML = popupStr;
            popup.setPosition(feature["values_"]["geometry"]["flatCoordinates"]);
          } else if (typeof(feature["values_"]["properties"]["route"]) !== "undefined") {
            // Crew
            popupStr += "Name: " + feature["values_"]["name"];
            popupStr += "<br\>IotId: " + feature["values_"]["@iot.id"];
            popupStr += "<br\>Route: " + feature["values_"]["properties"]["route"];

            popup.getElement().innerHTML = popupStr;
            popup.setPosition(feature["values_"]["geometry"]["flatCoordinates"]);
          } else {
            // Route or unknown element
            popup.setPosition(undefined);
          }


          M.addOverlay(popup);
          return [feature,layer];
      }, {
        hitTolerance: 3
      });
      if (!hit) {
        popup.setPosition(undefined);
      }
    });

    var thing_locations = new Map();  //map crew id to location
    var things = new Map(); //map crew id to props
    var thing_ids = [];

    function sendDataRequest() {
      // console.log("sent data requests");
      LoadMapData(things, thing_ids, thing_locations, bots_healthy_source,
                  bots_warning_source, bots_urgent_source, bots_unknown_source,
                  bots_needsparts_source, crews_source, routes_source);
      setTimeout(sendDataRequest, 60000);
    };
    sendDataRequest();
  },
  props: {
    healthyLayerOn: Boolean,
    warningLayerOn: Boolean,
    urgentLayerOn: Boolean,
    unknownLayerOn: Boolean,
    needsPartsLayerOn: Boolean,
    crewLayerOn: Boolean,
    routeLayerOn: Boolean
  },
  watch: {
    healthyLayerOn: function(newVal, oldVal) {
      bots_healthy_layer.setVisible(newVal);
    },
    warningLayerOn: function(newVal, oldVal) {
      bots_warning_layer.setVisible(newVal);
    },
    urgentLayerOn: function(newVal, oldVal) {
      bots_urgent_layer.setVisible(newVal);
    },
    unknownLayerOn: function(newVal, oldVal) {
      bots_unknown_layer.setVisible(newVal);
    },
    needsPartsLayerOn: function(newVal, oldVal) {
      bots_needsparts_layer.setVisible(newVal);
    },
    crewLayerOn: function(newVal, oldVal) {
      crews_layer.setVisible(newVal);
    },
    routeLayerOn: function(newVal, oldVal) {
      routes_layer.setVisible(newVal);
    }
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

#popup {
  /*width: 20px;*/
  background-color: black;
  color: #fff;
  text-align: center;
  padding: 3px 5px;
  border-radius: 6px;
}

#popup::after {
  content: " ";
  position: absolute;
  top: 100%; /* At the bottom of the tooltip */
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: black transparent transparent transparent;
}
</style>
