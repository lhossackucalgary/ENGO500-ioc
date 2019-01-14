import Vue from 'vue'
import L from 'leaflet'

// Leaflet
// const Leaf = window.L
delete L.Icon.Default.prototype._getIconUrl

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
})

export default Vue.component('map-view', {
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
})
