<template lang="html">
  <div>
    <div id="map">
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      map: [],
      markers: null
    }
  },
  mounted () {
    this.$nextTick(function () {
      const map = L.map('map').setView([51.505, -0.09], 13)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map)
      L.marker([51.5, -0.09]).addTo(map).bindPopup('A pretty CSS3 popup.<br> Easily customizable.').openPopup()
    })
  }
}
</script>

<style scoped>
@import "@/../../node_modules/leaflet/dist/leaflet.css"

#map
  width: 100%
  height: 400px
  font-weight: bold
  font-size: 13px
  text-shadow: 0 0 2px #fff
  .leaflet-shadow-pane > .leaflet-marker-shadow
    display: none
</style>

<!-- Add "scoped" attribute to limit CSS to this component only
<style scoped>
#mapid { height: 200px; }

h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
-->
