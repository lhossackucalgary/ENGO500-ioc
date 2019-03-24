<template>
  <div class="">
    <h2>Map Layers</h2>
    <ul>
      <li>Robot
        <ul>
          <li><label><img v-bind:src="require('@/assets/Healthy.png')" alt="Healthy" style="height:1.5em">
            <input type="checkbox" v-on:click="toggleHealthy" checked>Healthy</label>
          </li>
          <li><label><img :src="require('@/assets/Warning.png')" alt="Warning" style="height:1.5em">
            <input type="checkbox" v-on:click="toggleWarning" checked>Warning</label>
          </li>
          <li><label><img :src="require('@/assets/Urgent.png')" alt="Urgent" style="height:1.5em">
            <input type="checkbox" v-on:click="toggleUrgent" checked>Urgent</label>
          </li>
          <li><label><img :src="require('@/assets/Unknown.png')" alt="Unknown" style="height:1.5em">
            <input type="checkbox" v-on:click="toggleUnknown" checked>Unknown</label>
          </li>
          <li><label><img :src="require('@/assets/NeedsParts.png')" alt="Needs Parts" style="height:1.5em">
            <input type="checkbox" v-on:click="toggleNeedsParts" checked>Needs Parts</label>
          </li>
        </ul>
      </li>
      <li>Maintenance Crew
        <ul>
          <li><label><img :src="require('@/assets/Crew.png')" alt="Needs Parts" style="height:1.5em">
            <input type="checkbox" v-on:click="toggleCrews" checked>Crews</label>
          </li>
        </ul>
      </li>
      <li>Route
        <ul>
          <li><label><img :src="require('@/assets/Route.png')" alt="Needs Parts" style="height:1.5em">
            <input type="checkbox" v-on:click="toggleRoutes" checked>Routes</label>
          </li>
        </ul>
      </li>
    </ul>
    <hr>
    <hr>
  </div>
</template>

<script>
export default {
  data() {
    return {
      healthy: true,
      warning: true,
      urgent: true,
      unknown: true,
      needs_parts: true,
      crews: true,
      routes: true
    }
  },
  methods: {
    toggleHealthy:function(){
      if (this.healthy === true) {
        this.healthy = false;
      } else {
        this.healthy = true;
      }
      this.$emit('toggleHealthy', this.healthy);
    },
    toggleWarning:function(){
      if (this.warning === true) {
        this.warning = false;
      } else {
        this.warning = true;
      }
      this.$emit('toggleWarning', this.warning);
    },
    toggleUrgent:function(){
      if (this.urgent === true) {
        this.urgent = false;
      } else {
        this.urgent = true;
      }
      this.$emit('toggleUrgent', this.urgent);
    },
    toggleUnknown:function(){
      if (this.unknown === true) {
        this.unknown = false;
      } else {
        this.unknown = true;
      }
      this.$emit('toggleUnknown', this.unknown);
    },
    toggleNeedsParts:function(){
      if (this.needs_parts === true) {
        this.needs_parts = false;
      } else {
        this.needs_parts = true;
      }
      this.$emit('toggleNeedsParts', this.needs_parts);
    },
    toggleCrews:function(){
      if (this.crews === true) {
        this.crews = false;
      } else {
        this.crews = true;
      }
      this.$emit('toggleCrews', this.crews);
    },
    toggleRoutes:function(){
      if (this.routes === true) {
        this.routes = false;
      } else {
        this.routes = true;
      }
      this.$emit('toggleRoutes', this.routes);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
  margin-top: 5px;
  margin-bottom: 5px;
}
ul {
  list-style-type: none;
  padding-left: 30px;
  margin-top: 5px;
  margin-bottom:5px;
  text-align: left;
}
a {
  color: #42b983;
}
</style>
