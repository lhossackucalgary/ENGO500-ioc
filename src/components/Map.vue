<template>
    <div>
        <map-view></map-view>
        <map-layers></map-layers>
        <map-maint-summary></map-maint-summary>
        <map-selected-items></map-selected-items>
        <map-crew-info></map-crew-info>
    </div>
</template>

<script>
import MapCrewInfo from './MapComponents/MapCrewInfo.vue'
import MapLayers from './MapComponents/MapLayers.vue'
import MapMaintenanceSummary from './MapComponents/MapMaintenanceSummary.vue'
import MapSelectedItems from './MapComponents/MapSelectedItems.vue'
import MapView from './MapComponents/MapView.vue'

export default {
  name: 'Map',
  components: {
    'map-crew-info': MapCrewInfo,
    'map-layers': MapLayers,
    'map-maint-summary': MapMaintenanceSummary,
    'map-selected-items': MapSelectedItems,
    'map-view': MapView
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
