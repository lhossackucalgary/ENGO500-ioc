/* eslint-disable */
<template>
    <div>
        <div id="div_visuals">
            <div class="analytics-nav">
                <div class="an-nav-center">
                    <router-link to="/analytics/sys-summary" class="an-nav-link">System Summary</router-link>
                    <router-link to="/analytics/robot-health" class="an-nav-link">Robot Health</router-link>
                    <router-link to="/analytics/cpu-temp" class="an-nav-link">CPU Temperature</router-link>
                    <router-link to="/analytics/power-draw" class="an-nav-link">Power Draw</router-link>
                    <router-link to="/analytics/hist-data" class="an-nav-link">Historical Data</router-link>
                </div>
            </div>
            <div class="analytics-vis">
                <router-view></router-view>
            </div>
        </div>
    </div>
</template>

<script>
//<p style="white-space: pre-line;">{{ message }}</p>

import * as d3 from 'd3'

var TEMPERATURE_DATA = [];
var CURRENT_DATA = [];
/* --------------------------------------------------------------------------------------------- */
/* -------------------------------------------- EXPORT ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

export default {
  name: 'Analytics',
  mounted () {
    this.getData();
  },
  data () {
    return {
      msg: '',
      _data1: this._data1,
      _vis_height: this._vis_height,
      _vis_width: this._vis_width,
      PADDING_FOR_LABELS: this.PADDING_FOR_LABELS,
      obs: [],
      ds: [],
      th: [],
    }
  },
  methods: {
    loadObservations(){
        //create object to hold observation id, result, and time
        var obj_obs = function(id, result, time) {
            this.id = id;
            this.result = result;
            this.time = time;
        }
        //create an object with null values to hold resulting obs
        var obs = [];
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var r = JSON.parse(xhttp.responseText).value;
                r.forEach(result => {
                    var ob = new obj_obs(result['@iot.id'], result['result'], result['resultTime']);
                    obs.push(ob);
                });

            }
        };
        xhttp.open("GET", "http://routescout.sensorup.com/v1.0/Observations?$top=5000", true);
        xhttp.send();
        return obs;
    },

    loadDatastreams_Obs(obs_all){
        var dsobs = [];
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {

            if (this.readyState == 4 && this.status == 200) {
                var r = JSON.parse(xhttp.responseText).value;
                //object to hold datastream:id, type, and list of observation ids
                var Obj_ds_ob = function(a, b, c){
                    this.id = a;
                    this.type = b //either T, P, or H (temp, pressure, or HP)
                    this.obids = c;
                }

                for (var i = 0; i < r.length; i++) {
                    var dsid = r[i]['@iot.id']; //datastream id at i

                    var desc = r[i]['description'];

                    //get type of the datastream at i
                    var type = null;
                    if (desc === "Datastream for recording pressure") {
                        type = 'P';
                    } else if (desc === "Datastream for recording temperature") {
                        type = 'T';
                    } else if (desc === "Health percentage") {
                        type = 'H';
                    } else {
                        console.error("datastream does not have valid type: " + desc);
                    }

                    //get observations from datastream at i
                    var obs = r[i]['Observations'];//obs array at i
                    var obids = [];
                    for (var j = 0; j < obs.length; j++) {
                        var obid = obs[j]['@iot.id'];//obid at datastream i,

                        //get the info of the obs
                        obs_all.forEach(res => {
                            if (obid == res.id) {
                                //push to obids, which now contains obs info (id, result, time)
                                obids.push(res);
                            }
                        })
                    }

                    //create new obj_ds_ob to hold all of the data
                    var dsob = new Obj_ds_ob(dsid,type,obids);
                    //add to array of datastream w obs
                    dsobs.push(dsob);
                }
            }
        };
        xhttp.open("GET", "http://routescout.sensorup.com/v1.0/Datastreams?$top=500&$expand=Observations", true);
        xhttp.setRequestHeader("Authorization", "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI=");
        xhttp.setRequestHeader("Content-Type", "application/json; charset=utf-8");
        xhttp.send();
        return dsobs;
    },

    loadThing_Datastreams_Obs(dsobs){
        var thdsobs = [];
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var r = JSON.parse(xhttp.responseText).value;

                //object to hold thing: id, name, desc, status, and list of ds objects
                var obj_th_ds_obs = function(id, name, desc, stat, ds) {
                    this.id = id;
                    this.name = name;
                    this.desc = desc;
                    this.status = stat;
                    this.ds = ds;
                }

                for (var i = 0; i < r.length; i++) {
                    var thid = r[i]['@iot.id'];
                    var thname = r[i]['name'];
                    var thdesc = r[i]['description'];
                    var thstat = r[i]['properties']['status'];
                    var thds = [];

                    //get all datastreams of thing at i
                    var allds = r[i]['Datastreams'];
                    for (var j = 0; j < allds.length; j++) {
                        var dsid = allds[j]['@iot.id'];

                        //loop through dsobs to find the dsob matching the current dsid
                        for (var k = 0; k < dsobs.length; k++) {
                            if (dsid == dsobs[k].id) {
                                thds.push(dsobs[k]);
                            }
                        }
                    }

                    //create new obj_th_ds_obs to hold all of the thing info
                    var thdsob = new obj_th_ds_obs(thid, thname, thdesc, thstat, thds);
                    //append to final list of all things
                    thdsobs.push(thdsob);
                }
            }
        };
        xhttp.open("GET", "http://routescout.sensorup.com/v1.0/Things?$top=500&$expand=Datastreams", true);
        xhttp.setRequestHeader("Authorization", "Basic bWFpbjoxYTZhZjZkOC1hMDc0LTVlNDgtOTNiYi04ZGY3MDllZDE3ODI=");
        xhttp.setRequestHeader("Content-Type", "application/json; charset=utf-8");
        xhttp.send();
        return thdsobs;
    },
    obs_data_check() {
        if (this.obs.length > 0) {
            this.ds = this.loadDatastreams_Obs(this.obs);
        } else {
            setTimeout(this.obs_data_check, 500);
        }
    },
    ds_data_check() {
        if (this.ds.length > 0) {
            this.th = this.loadThing_Datastreams_Obs(this.ds);
        } else {
            setTimeout(this.ds_data_check, 500);
        }
    },
    th_data_check() {
        if (this.th.length > 0) {
            //console.log(th);
            this.saveData(this.th);
            this.$store.commit('updateTh', this.th);
        } else {
            setTimeout(this.th_data_check, 500);
        }
    },
    getData(){
        this.obs = this.loadObservations();
        this.obs_data_check();

        //check that ds is defined before running loadThing_Datastreams_Obs(ds)

        this.ds_data_check();
        this.th_data_check();
    },
    /* --------------------------------------------------------------------------------------------- */
    /* ------------------------------ API DATA TO OBSERVATION DATA --------------------------------- */
    /* --------------------------------------------------------------------------------------------- */

    saveData(th) {
        //clear old values from store
        this.$store.commit('clearRobotHealth');
        this.$store.commit('clearTemperatureData');
        this.$store.commit('clearCurrentData');
        this.$store.commit('clearAllRobotHealth');

        //extract latest health observation   
        var obj_rb = function(robot, health, date) {
            this.robot = robot;
            this.result = health;
            this.date = date;
        }
        for (var i = 0; i < th.length; i++) {
            var name = th[i].name.slice(0,5);
            //console.log(name);
            if (name === "robot") {
                var ds = th[i].ds;
                var health = null;
                var date = null;
                var rnum = "r"+th[i].name.slice(5);
                for (var j = 0; j < ds.length; j++) {
                    if (ds[j].type == 'H') {
                        health = ds[j].obids[0].result;
                        date = ds[j].obids[0].resultTime;
                    }
                }
                var rb = new obj_rb(rnum, health, date);
                this.$store.commit('pushRobotHealth', rb);

            }
        }

        //extract all robot health data
        for (var i = 0; i < th.length; i++) {
            var ds = th[i].ds;
            var rname = th[i].name;
            for (var j = 0; j < ds.length; j++) {
                if (ds[j].type == 'H') {
                ds[j].obids.forEach(ob => {
                    result = ob.result;
                    date = ob.time;
                    var h_obs = new obj_rb(rname, result, date);
                    this.$store.commit('pushAllRobotHealth', h_obs);
                });
                }
            }
        }

        //extract all temperature observations
        //{ "robot" : "robot_1", "date" : "2019-02-07T18:02:05.000Z", "result" : 30 },

        var obj_temp = function(robot, date, result) {
            this.robot = robot;
            this.date = date;
            this.result = result;
        }
        for (var i = 0; i < th.length; i++) {
            var name = th[i].name.slice(0,5);
            if (name === "robot") {
                var ds = th[i].ds;
                var result = null;
                var date = null;
                var rname = th[i].name;
                // loop through all ds of the robot
                for (var j = 0; j < ds.length; j++) {
                    if (ds[j].type == 'T') {
                        // loop through all obs of the temp ds
                        for (var k = 0; k < ds[j].obids.length; k++) {
                            result = ds[j].obids[k].result;
                            date = ds[j].obids[k].time;
                            var t_obs = new obj_temp(rname, date, result);
                            this.$store.commit('pushTemperatureData', t_obs);
                        }
                    }
                }
            }
        }

        //extract all current (previously pressure) observations
        var obj_curr = function(robot, date, result) {
            this.robot = robot;
            this.date = date;
            this.result = result;
        }
        for (var i = 0; i < th.length; i++) {
            var name = th[i].name.slice(0,5);
            if (name === "robot") {
                var ds = th[i].ds;
                var result = null;
                var date = null;
                var rname = th[i].name;
                // loop through all ds of the robot
                for (var j = 0; j < ds.length; j++) {
                    if (ds[j].type == 'P') {
                        // loop through all obs of the temp ds
                        for (var k = 0; k < ds[j].obids.length; k++) {
                            result = ds[j].obids[k].result;
                            date = ds[j].obids[k].time;
                            var c_obs = new obj_curr(rname, date, result);
                            this.$store.commit('pushCurrentData', c_obs);
                        }
                    }
                }
            }
        }

    },
        
  },
  route: {
      activate() {
          graph();
      }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* importing fonts from Google Font API */
@import url('https://fonts.googleapis.com/css?family=Major+Mono+Display');
@import url('https://fonts.googleapis.com/css?family=Sarabun:300,300i,400,700');

html {
    background: darkturquoise;
    min-width: 1280px;
    min-height: 720px;
    overflow: auto;

    font-family: "Sarabun", sans-serif;
    font-weight: 300;
    color: white;
    letter-spacing: 0.1em;
}

body {
    padding: 20px;
}

h1{
    font-family: "Major Mono Display", sans-serif;
    font-size: 3em;

    color: white;
    letter-spacing: normal;
    text-transform: lowercase;

    margin-bottom: 0;
    padding-bottom: 0;
}

h2 {
    font-family: "Major Mono Display", sans-serif;
    font-size: 1.5em;
    letter-spacing: normal;
    text-transform: lowercase;
}

h3 {
    color: black;
    font-family: "Sarabun", sans-serif;
    font-size: 1.5em;
    font-weight: 400;
    letter-spacing: normal;
    text-transform: capitalize;
    width: 90%;
    margin: 20px auto;
}
.analytics-nav {
    background: lightgrey;
    height: 60px;
    position: fixed;
    top: 60px;
    left: 0;
    width: 100%;
    overflow: hidden;
}
.an-nav-center {
    float: center;
    
    width: 100%;
    height: 60px;
    padding: 12px;
    text-align: center;
}
.an-nav-link {
    padding: 15px;
    font-size: 22px;
    font-weight: bold;
    color: white;
    text-decoration: none;
    text-align:center;
}
.an-nav-link:hover {
    text-decoration: underline;
    color:#2c3e50;
}
.analytics-vis {
    position: fixed;
    top: 120px;
    width: 100%;
}
/* styling an element through its ID */
div#div_page_desc {
    margin: 10px;
}

div#div_data_desc {
    background: white;
    box-sizing: border-box;
    padding: 10px 20px;

    color: black;
}

div#div_visuals {
    background: white;
    background-clip: content-box;
    width: 100%;
    height: 100%;
    /*min-height: 100px;*/
    /*max-height: 550px;*/
    box-sizing: border-box;
    /*padding: 10px;*/
    overflow-y:scroll;
    position:fixed !important;
    position:absolute;
    top:60px;
    right:0;
    bottom:60px;
    left:0;
}

div#div_buttons {
    padding: 20px;
}

div.vis_div {
    float: left;
    width: 85%;
    height: 470px;
    overflow-y: scroll;
    overflow-x:hidden !important;
}

div.vis_btn {
    float: left;
    width: 15%;
    height: 430px;
    background: white;
}

button.cat {
    display: block;
}

button {
    background: white;
    border: none;
    height: 30px;
    padding: 0px 10px;

    font-family: "Sarabun", sans-serif;
    font-weight: 400;
    font-size: 1em;
    letter-spacing: 0.1em;
}

button:hover {
    background: darkturquoise;
    cursor: pointer;
}

button:focus {
    outline: 0;
}
.svg_boxes {
    background: white;
    /*border: 1px solid lightgrey;*/
    display: block;
    width: 95%;
    min-width: 800px;
    min-height: 400px;
    /*box-sizing: border-box;*/
    margin: 10px auto;
    overflow-x:hidden;
}
.spacer {
    height: 100px;
    float: left;
    width: 100%;
}
</style>

<!--
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
-->
