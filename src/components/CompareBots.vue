/* eslint-disable */
<template>
  <div class="">
    <h2>Compare Robots Page</h2>
    <p>{{$store.state.selected_items}}</p>
  </div>
</template>

<script>
import * as d3 from 'd3'

var th;
var ROBOT_HEALTH;
var TEMPERATURE_DATA;
var CURRENT_DATA;

/* --------------------------------------------------------------------------------------------- */
/* ------------------------------------ LOAD DATA FROM API ------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function loadObservations(){
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
}

function loadDatastreams_Obs(obs_all){
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
}

function loadThing_Datastreams_Obs(dsobs){
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
}

function getData(){
    var obs = loadObservations();

    var ds = [];
    function obs_data_check() {
        if (obs.length > 0) {
            ds = loadDatastreams_Obs(obs);
        } else {
            setTimeout(obs_data_check, 500);
        }
    }
    obs_data_check();

    th = [];
    //check that ds is defined before running loadThing_Datastreams_Obs(ds)
    function ds_data_check() {
        if (ds.length > 0) {
            th = loadThing_Datastreams_Obs(ds);
        } else {
            setTimeout(ds_data_check, 500);
        }
    }
    ds_data_check();
    
    
    function th_data_check() {
        if (th.length > 0) {
            console.log(th);
            //saveData(th);
        } else {
            setTimeout(th_data_check, 500);
        }
    }
    th_data_check();
}

/* --------------------------------------------------------------------------------------------- */
/* ------------------------------ API DATA TO OBSERVATION DATA --------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function saveData() {
    var compBot_id = this.$store.state.selected_items;
    //extract latest health observation
    //{ "robot" : "robot_1", "health" : 90, "pressure" : 40, "temperature" : 20}
    ROBOT_HEALTH = [];
    var obj_rb = function(robot, date, health) {
        this.robot = robot;
        this.date = date;
        this.health = health;
    }
    for (var i = 0; i < th.length; i++) {
      compBot_id.forEach(cid => {
        if (cid = th[i].id) {
          var ds = th[i].ds;
            var health = null;
            var rname = th[i].name;
            for (var j = 0; j < ds.length; j++) {
              if (ds[j].type == 'H') {
                health = ds[j].obids[0].result;
                ds[j].obids.forEach(ob => {
                  result = ob.result;
                  date = ob.time;
                  var h_obs = new obj_temp(rname, date, result);
                  ROBOT_HEALTH.push(h_obs);
                });
              }
            }
        }
      });
    }//CHECK THIS

    //extract all temperature observations
    //{ "robot" : "robot_1", "date" : "2019-02-07T18:02:05.000Z", "result" : 30 },
    TEMPERATURE_DATA = [];
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
                    //console.log(ds[j].id);
                    // loop through all obs of the temp ds
                    for (var k = 0; k < ds[j].obids.length; k++) {
                        result = ds[j].obids[k].result;
                        date = ds[j].obids[k].time;
                        var t_obs = new obj_temp(rname, date, result);
                        TEMPERATURE_DATA.push(t_obs);
                    }
                }
            }
        }
    }

    //extract all current (previously pressure) observations
    CURRENT_DATA = [];
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
                    //console.log(ds[j].id);
                    // loop through all obs of the temp ds
                    for (var k = 0; k < ds[j].obids.length; k++) {
                        result = ds[j].obids[k].result;
                        date = ds[j].obids[k].time;
                        var c_obs = new obj_curr(rname, date, result);
                        CURRENT_DATA.push(c_obs);
                    }
                }
            }
        }
    }
    /*
    function temp_data_check() {
        if (TEMPERATURE_DATA.length > 0) {
            console.log(TEMPERATURE_DATA);
        } else {
            setTimeout(temp_data_check, 500);
        }
    }
    temp_data_check();
    */
    
}

/* --------------------------------------------------------------------------------------------- */
/* ------------------------------------- HEALTH BAR CHART -------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

export default {
  name: 'CompareBots',
  data () {
    return {

    }
  },
  mounted () {
    console.log(this.$store.state.selected_items);
    getData();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
