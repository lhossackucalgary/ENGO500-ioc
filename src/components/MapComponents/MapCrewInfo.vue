<template>
  <div id="crewinfopane" ref="crewinfopane">
    <h2>{{name}}</h2>
    <p>Iot ID: {{iotid}}</p>
    <p>Location: ({{geometry[0].toFixed(6)}}, {{geometry[1].toFixed(6)}})</p>
    <ol>Route:
      <li v-for="(i, index) in route"><button v-on:click="deleteBot(route.indexOf(i))">x</button>{{i}}<input v-model="formInputs[index]" type="text" style="width: 50px;"></input><button v-on:click="addBotForm(index)">+</button></li>
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
      route: Array,
      formInputs: Array
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
    },
    deleteBot: function(i) {
      this.route.splice(i, 1);
    },
    addBotForm: function(i) {
      let inputVal = parseInt(this.formInputs[i]);
      var crewInfoThis = this;
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = (function(crewInfoThis, id, index) {
          return function() {
          if (this.readyState == 4 && this.status >= 200 && this.status < 300) {
            crewInfoThis.route.splice(index+1, 0, id);

            let data = {"description": "[]", "properties": {"route": crewInfoThis.route}};

            var xhttp2 = new XMLHttpRequest();
            xhttp2.onreadystatechange = function() {
              if (this.readyState == 4 && this.status >= 200 && this.status < 300) {
                // send msg to map layer to reload map data
                alert("Route successfully updated.");
              } else if (this.readyState == 4) {
                alert("Failed to update route. Please refresh and try again.");
              }
            }

            xhttp2.open("PATCH", "http://routescout.sensorup.com/v1.0/Things(" + crewInfoThis.iotid + ")", true);
            xhttp2.setRequestHeader("Authorization", "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI=");
            xhttp2.setRequestHeader("Content-Type", "application/json; charset=utf-8");
            xhttp2.send(JSON.stringify(data));

          } else if (this.readyState == 4) {
            alert("iotid " + id + " is not a valid iotid.");
          }
        }
      })(crewInfoThis, inputVal, i);

      xhttp.open("GET", "http://routescout.sensorup.com/v1.0/Things(" + inputVal + ")", true);
      xhttp.send();
    }
  },
  watch: {
    route: function(newVal, oldVal) {

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
