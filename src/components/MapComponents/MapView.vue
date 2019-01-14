<template>
    <div id="map"></div>
</template>

<script>
import {Map, View} from 'ol'
import TileLayer from 'ol/layer/Tile'
import XYZ from 'ol/source/XYZ'

export default {
  mounted () {
    var M = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new XYZ({
            url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'
          })
        })
      ],
      view: new View({
        center: [0, 0],
        zoom: 2
      })
    })
    console.log(M)
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import url("https://openlayers.org/en/latest/css/ol.css")

#map {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 100%;
}
</style>
