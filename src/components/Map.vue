<template>
    <div>
      <div id="mapcontainer">
        <map-view v-bind:healthyLayerOn="healthyOn"
                  v-bind:warningLayerOn="warningOn"
                  v-bind:urgentLayerOn="urgentOn"
                  v-bind:unknownLayerOn="unknownOn"
                  v-bind:needsPartsLayerOn="needsPartsOn"
                  v-bind:crewLayerOn="crewsOn"
                  v-bind:routeLayerOn="routesOn"
                  ></map-view>
      </div>
      <div id="layerselcont">
        <div id="layercontainer">
          <map-layers v-on:toggleHealthy="updateHealthy($event)"
                      v-on:toggleWarning="updateWarning($event)"
                      v-on:toggleUrgent="updateUrgent($event)"
                      v-on:toggleUnknown="updateUnknown($event)"
                      v-on:toggleNeedsParts="updateNeedsParts($event)"
                      v-on:toggleCrews="updateCrews($event)"
                      v-on:toggleRoutes="updateRoutes($event)"
                      ></map-layers>
        </div>
        <div id="selectedcontainer">
          <map-selected-items></map-selected-items>
        </div>
      </div>
      <div id="maintcontainer">
        <map-maint-summary></map-maint-summary>
      </div>
      <div id="crewinfo">
        <map-crew-info></map-crew-info>
      </div>
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
  },
  data() {
    return {
      healthyOn: true,
      warningOn: true,
      urgentOn: true,
      unknownOn: true,
      needsPartsOn: true,
      crewsOn: true,
      routesOn: true
    }
  },
  methods: {
    updateHealthy:function(status) {
      this.healthyOn = status;
    },
    updateWarning:function(status) {
      this.warningOn = status;
    },
    updateUrgent:function(status) {
      this.urgentOn = status;
    },
    updateUnknown:function(status) {
      this.unknownOn = status;
    },
    updateNeedsParts:function(status) {
      this.needsPartsOn = status;
    },
    updateCrews:function(status) {
      this.crewsOn = status;
    },
    updateRoutes:function(status) {
      this.routesOn = status;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#mapcontainer {
  position: fixed;
  top: 60px;
  left: 250px;
  width: 100%;
  height: 100%;
}

#layerselcont {
  position: fixed;
  width: 250px;
  top: 60px;
  left: 0;
  height: 100%;
}

#layercontainer {
  height: 50%;
  background-color: white;
  overflow-y: scroll;
}

#selectedcontainer {
  height: 50%;
  background-color: white;
  overflow-y: scroll;
}

#maintcontainer {

}

#crewinfo {

}
</style>
