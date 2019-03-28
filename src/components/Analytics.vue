/* eslint-disable */
<template>
        <div id="div_visuals">
          <router-link to="/analytics/sys-summary">System Summary</router-link>
          <router-link to="/analytics/robot-health">Robot Health</router-link>
          <router-link to="/analytics/cpu-temp">CPU Temperature</router-link>
          <router-link to="/analytics/power-draw">Power Draw</router-link>
          <router-link to="/analytics/hist-data">Historical Data</router-link>
          <router-view></router-view>

            <div class="spacer"></div>
      </div>
</template>

<script>
//<p style="white-space: pre-line;">{{ message }}</p>

import * as d3 from 'd3'


/* --------------------------------------------------------------------------------------------- */
/* ------------------------------- INITIALIZE GLOBAL VARIABLES --------------------------------- */
/* --------------------------------------------------------------------------------------------- */

const WIDTH = 1000; //800
const HEIGHT = 300; //100
const PAD = 10;
const MARGIN = 50;
const _margin = ({top: 10, right: 0, bottom: 30, left: 40});
const PADDING_FOR_LABELS = 90;

const SAMPLE_DATA = [
    { "month" : "January", "point" : [5, 20], "r" : 10 },
    { "month" : "February", "point" : [480, 90], "r" : 1 },
    { "month" : "March", "point" : [250, 50], "r" : 3 },
    { "month" : "April", "point" : [100, 33], "r" : 3 },
    { "month" : "May", "point" : [330, 95], "r" : 4 },
    { "month" : "June", "point" : [300, 40], "r" : 8 },
    { "month" : "July", "point" : [410, 35], "r" : 6 },
    { "month" : "August", "point" : [475, 44], "r" : 4 },
    { "month" : "September", "point" : [25, 67], "r" : 1 },
    { "month" : "October", "point" : [85, 21], "r" : 5 },
    { "month" : "November", "point" : [220, 88], "r" : 10 },
    { "month" : "December", "point" : [400, 4], "r" : 7 },
];

var CURRENT_DATA = [];

var TEMPERATURE_DATA = [];

/* global variables */
var _data1;
var _vis_width = 1000;
var _vis_height = 300;
var svg1;
var bar1;
var _bar1_width = 30;
var _bar1_offset = 5;
var vis1_x;
var vis1_y;
var _vis1;
var _vis2;
var _vis3;
var _vis4;
var _vis5;
var _vis6;

var parseTime = d3.timeParse("%H:%M %p");
var parseDate = d3.timeParse("%Y-%m-%d");
var colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#fabebe', '#008080', '#e6beff', '#9a6324', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080',
    '#806060', '#ff2200', '#330e00', '#e59173', '#993d00', '#4d4139', '#d97400', '#f2ba79', '#d9bfa3', '#ffaa00', '#734d00', '#332200', '#bfb300', '#6f7339', '#ccff00', '#1b3300', '#639926', '#d9ffbf', '#3df23d', '#304030', '#00733d', '#00f2a2',
    '#2db3aa', '#005c73', '#40d9ff', '#8fb6bf', '#002233', '#003d73', '#3995e6', '#001180', '#070033', '#574d99', '#7e39e6', '#3b264d', '#6b0073', '#b086b3', '#f23de6', '#b2005f', '#33001b', '#73002e', '#f27999', '#b20018']; // '#ffffff', '#000000',
//var data = [10, 20, 30 , 40, 50];

var msg_vis2 = "robot1\nrobot2\nrobot3\nrobot4";

var HPyRange;
var HPyDomain;
var HPxRange;
var HPxLength;

/* --------------------------------------------------------------------------------------------- */
/* -------------------------------------- SET UP VIS 4 ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function setupVis4(){
  let xScale = d3.scaleLinear()
        .domain([0, d3.max(SAMPLE_DATA, function(d) { return d.point[0]; })])
        .range([MARGIN, WIDTH-MARGIN]);

    let yScale = d3.scaleLinear()
        .domain([0, d3.max(SAMPLE_DATA, function(d) { return d.point[1]; })])
        .range([MARGIN, HEIGHT-MARGIN]);

    // Create a scale using d3.scaleQuantize to bin values from the domain
    // into categories coloured as deeppink, pink, paleturquoise, and darkturquoise
    // the values are divided equally to each category
    // e.g., if the upper limit to the domain is 100, and we specified 4 categories,
    // then the first category will have values between 0 and 25, then 25 and 50, etc.
    let colorScale = d3.scaleQuantize()
        .domain([0, d3.max(SAMPLE_DATA, function(d) { return d.r; })])
        .range(["deeppink", "pink", "paleturquoise", "darkturquoise"]);

    let sizeScale = d3.scalePow()
        .exponent(2)
        .domain([0, d3.max(SAMPLE_DATA, function(d) { return d.r; })])
        .range([5, 50]); // 0 to 50 pixels

    //Create SVG element
    let svg = d3.select("#vis4")
        .attr("width", WIDTH)
        .attr("height", HEIGHT);

    svg.selectAll("circle")
        .data(SAMPLE_DATA)
        .enter()
        .append("circle")
        .attr("cx", function(d) {
            return xScale(d.point[0]);
        })
        .attr("cy", function(d) {
            return yScale(d.point[1]);
        })
        .attr("r", function(d){
            return sizeScale(d.r);
        })
        .style("fill", function(d){
            return colorScale(d.r);
        })
        .style("stroke", "none");

    svg.selectAll("text")
        .data(SAMPLE_DATA)
        .enter()
        .append("text")
        .text(function(d) {
            return d.month;
        })
        .attr("x", function(d) {
            return xScale(d.point[0]) + sizeScale(d.r) + (PAD/2);
        })
        .attr("y", function(d) {
            return yScale(d.point[1]);
        })
        .attr("font-family", "sans-serif")
        .attr("font-size", "11px")
        .attr("fill", "teal")
        .style("text-anchor", "start")
        .style("alignment-baseline", "middle");
}

/* --------------------------------------------------------------------------------------------- */
/* -------------------------------------------- EXPORT ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

export default {
  name: 'Analytics',
  mounted () {
    this.getData();
    //setupVis2();
    //setupVis3();
    setupVis4();
    //setupVis5();
    //setupVis6();
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
        //extract latest health observation   
        var obj_rb = function(robot, health) {
            this.robot = robot;
            this.health = health;
        }
        for (var i = 0; i < th.length; i++) {
            var name = th[i].name.slice(0,5);
            //console.log(name);
            if (name === "robot") {
                var ds = th[i].ds;
                var health = null;
                var rnum = "r"+th[i].name.slice(5);
                for (var j = 0; j < ds.length; j++) {
                    if (ds[j].type == 'H') {
                        health = ds[j].obids[0].result;
                    }
                }
                var rb = new obj_rb(rnum, health);
                this.$store.commit('pushRobotHealth', rb);

            }
        }

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
