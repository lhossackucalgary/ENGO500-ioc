<template>
  <div id="crewinfopane" ref="crewinfopane">
    <h2>{{name}}</h2>
    <p>Iot ID: {{iotid}}</p>
    <p>Location: ({{geometry[0].toFixed(6)}}, {{geometry[1].toFixed(6)}})</p>
    <ol>Route:
      <li v-for="i in route" >{{i}}</li>
    </ol>

    <button id="closecrewinfopanebtn" name="button" v-on:click="closeCrewInfo">&rarr;</button>
  </div>
</template>

<script>
export default {
  components: {

  },
  created(){
    this.feature = {};
    this.geometry = [0,0];
    this.iotid = -1;
    this.name = "";
    this.route = [];
    document.addEventListener('crewShowMore', this.crewShowMore);
  },
  data() {
    return {
      feature: Object,
      geometry: Array,
      iotid: Number,
      name: String,
      route: Array
    }
  },
  methods: {
    crewShowMore:function(e) {
      this.$refs["crewinfopane"].style = "visibility: visible;";
      this.feature = e.detail;
      this.geometry = e.detail.geometry;
      this.iotid = e.detail.iotid;
      this.name = e.detail.name;
      this.route = e.detail.properties.route;
    },
    closeCrewInfo:function() {
      this.$refs["crewinfopane"].style = "visibility: hidden;";
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#crewinfopane {
  visibility: hidden;
  position: absolute;
  right: 0px;
  top: 0px;
  height: 100%;
  width: 25%;
  background-color: white;
  text-align: left;
}

#closecrewinfopanebtn {
  position: absolute;
  left: 3px;
  top: 3px;
}
h1, h2 {
  font-weight: normal;
  text-align: center;
  text-decoration: underline;
}
ul {
  list-style-type: none;
  padding: 0;
}
ol {
  padding-left: 15px;
}
li {
  display: block;
  margin: 5px 20px;
}
a {
  color: #42b983;
}
p {
  padding-left: 15px;
}
</style>
