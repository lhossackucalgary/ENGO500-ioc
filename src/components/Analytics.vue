/* eslint-disable */
<template>
        <div id="div_visuals">
            <div>
                <h3>Robot Summary</h3>
                <div id="vis7" class="vis_div"></div>
            </div>
            <div>
                <div id="vis1box" class="vis_div">
                    <h3 class="head">Robot Health</h3>
                    <svg id="vis1" class="svg_boxes"></svg>
                </div>
                <div id="vis1btn" class="vis_btn">
                    <div class="spacer"></div>
                    <button id="btn_name_ascending" class="cat" v-on:click="vis1_switch('name-ascending')">Name Ascending</button>
                    <button id="btn_val_ascending" class="cat" v-on:click="vis1_switch('value-ascending')">Value Ascending</button>
                    <button id="btn_val_descending" class="cat" v-on:click="vis1_switch('value-descending')">Value Descending</button>
                </div>
            </div>
            <div class="spacer"></div>
            <div>
                <div id="vis2box" class="vis_div">
                    <h3>Sensor807: Motor Power Draw</h3>
                    <svg id="vis2" class="svg_boxes"></svg>
                </div>
                <div id="vis2btn" class="vis_btn">
                    <p>Enter list of robot names: </p>
                    <textarea id="vis2textbox" v-model="message_v2" placeholder="robot1 robot2 ..."></textarea>
                    <br>
                    <button id="btn_vis2_update" class="cat" v-on:click="vis2_update()">Update Chart</button>
                </div>
            </div>
            <div class="spacer"></div>
            <div>
                <div id="vis3box" class="vis_div">
                    <h3>Sensor876: CPU Temperature</h3>
                    <svg id="vis3" class="svg_boxes"></svg>
                </div>
                <div id="vis3btn" class="vis_btn">
                    <p>Enter list of robot names: </p>
                    <textarea id="vis3textbox" v-model="message_v3" placeholder="robot1 robot2 ..."></textarea>
                    <br>
                    <button id="btn_vis3_update" class="cat" v-on:click="vis3_update()">Update Chart</button>
                </div>
            </div>
            <div class="spacer"></div>
            <div>
                <h3>Thermometer_236: Robot_1</h3>
                <svg id="vis5" class="svg_boxes"></svg>
            </div>
            <div class="spacer"></div>
            <div>
                <h3>Thermometer_236: Robot_2</h3>
                <svg id="vis6" class="svg_boxes"></svg>
            </div>
            <div class="spacer"></div>
            <div>
                <h3>Historical Data</h3>
                <svg id="vis4" class="svg_boxes"></svg>
            </div>
      </div>
</template>

<script>
//<p style="white-space: pre-line;">{{ message }}</p>

import * as d3 from 'd3'
import * as vega from 'vega'
import {default as vegaEmbed} from 'vega-embed'
import * as vegaLite from 'vega-lite'

/* --------------------------------------------------------------------------------------------- */
/* ------------------------------- INITIALIZE GLOBAL VARIABLES --------------------------------- */
/* --------------------------------------------------------------------------------------------- */

var ROBOT_HEALTH = [];

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

/* constants */
const WIDTH = 1000; //800
const HEIGHT = 300; //100
const PAD = 10;
const MARGIN = 50;
const _margin = ({top: 10, right: 0, bottom: 30, left: 40});
const PADDING_FOR_LABELS = 90;

/* global variables */
var _vis;
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
var _vis7data;
var parseTime = d3.timeParse("%H:%M %p");
var parseDate = d3.timeParse("%Y-%m-%d");
var colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#fabebe', '#008080', '#e6beff', '#9a6324', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080',
    '#806060', '#ff2200', '#330e00', '#e59173', '#993d00', '#4d4139', '#d97400', '#f2ba79', '#d9bfa3', '#ffaa00', '#734d00', '#332200', '#bfb300', '#6f7339', '#ccff00', '#1b3300', '#639926', '#d9ffbf', '#3df23d', '#304030', '#00733d', '#00f2a2',
    '#2db3aa', '#005c73', '#40d9ff', '#8fb6bf', '#002233', '#003d73', '#3995e6', '#001180', '#070033', '#574d99', '#7e39e6', '#3b264d', '#6b0073', '#b086b3', '#f23de6', '#b2005f', '#33001b', '#73002e', '#f27999', '#b20018']; // '#ffffff', '#000000',
//var data = [10, 20, 30 , 40, 50];
var th;
var msg_vis2 = "robot1\nrobot2\nrobot3\nrobot4";

var HPyRange;
var HPyDomain;
var HPxRange;
var HPxLength;


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
            //console.log(th);
            saveData(th);
        } else {
            setTimeout(th_data_check, 500);
        }
    }
    th_data_check();
}

/* --------------------------------------------------------------------------------------------- */
/* ------------------------------ API DATA TO OBSERVATION DATA --------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function saveData(th) {
    //extract latest health observation
    //{ "robot" : "robot_1", "health" : 90, "pressure" : 40, "temperature" : 20}
    ROBOT_HEALTH = [];
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
            ROBOT_HEALTH.push(rb);
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

// code modified from Scott Murray's example
// https://alignedleft.com/tutorials/d3/scales
function setupVis1(){
    if (ROBOT_HEALTH.length > 0) {
        _vis1 = new Healthplot();
        _vis1.svg = d3.select("#vis1");
        //match size of svg container in html
        _vis1.width = _vis1.svg.node().getBoundingClientRect().width != undefined ?
            _vis1.svg.node().getBoundingClientRect().width : _vis1.width; //if undefined
        _vis1.height = _vis1.svg.node().getBoundingClientRect().height;

        _vis1.data = ROBOT_HEALTH;
        _vis1.setupScales([_vis1.height - _margin.bottom, _margin.top], [0, 100], [0, _vis1.width - _margin.left], _vis1.data.length);
        _vis1.setupAxis();
        _vis1.createBars();
    } else {
        setTimeout(setupVis1, 500);
    }
}

var Healthplot = function(){
    this.data;
    this.olddata;
    this.width = WIDTH;
    this.height = HEIGHT;

    this.svg;
    this.bar;

    this.xAxisScale;
    this.xScale;
    this.yScale;

    this.xAxis;
    this.yAxis;
    this.gx;

    this.setupScales = function(yRange, yDomain, xRange, xLength){

        HPyRange = yRange;
        HPyDomain = yDomain;
        HPxRange = xRange;
        HPxLength = xLength;

        //kind of like the min and max value of range in last tut
        this.yScale = d3.scaleLinear()
            .domain(yDomain)
            .range(yRange);

        this.xScale = d3.scaleBand()
            .domain(d3.range(0, xLength))
            .rangeRound(xRange)
            .padding(0.1);

        this.xAxisScale = d3.scaleBand()
            .rangeRound(xRange) //[0, this.width - _margin.left]
            .domain(this.data.map(function(d){ return d.robot; }));

    };

    this.setupAxis = function(){
        this.yAxis = d3.axisLeft(this.yScale)
            .tickSize(-this.width);

        this.xAxis = d3.axisBottom(this.xAxisScale);

        this.svg.append("g")
            .attr("transform", `translate(${_margin.left}, 0)`)
            .attr("class", "y axis")
            .call(this.yAxis);

        this.gx = this.svg.append("g")
            .attr("transform", `translate(${_margin.left}, ${_vis1.height - _margin.bottom})`)
            .attr("class", "x axis")
            .call(this.xAxis);

        // x-axis label
        this.svg.append("text")
            .attr("x", this.width / 2)
            .attr("y", this.height - _margin.bottom / 2 + 15)
            .style("text-anchor", "middle")
            .text("Robot Name");

        // y-axis label
        this.svg.append("text")
            .attr("x", _margin.left)
            .attr("y", this.height/2)
            .attr("transform", `rotate(-90, ${_margin.left / 3}, ${this.height/2})`)
            .style("text-anchor", "middle")
            .text("Health (%)");

    }

    this.createBars = function() {
    this.bar = this.svg.selectAll("rect")
            .data(this.data)
            .enter()
            .append("rect")
                .attr("class", "bar")
                .style("fill","lightgreen")
                .attr("width", _vis1.xScale.bandwidth())
                .attr("height", function(d) { return (_vis1.height - _margin.bottom - _vis1.yScale(d.health)); })
                .attr("x", function(d, i) { return _vis1.xScale(i); })
                .attr("y", function(d) { return _vis1.yScale(d.health); })
                .attr("transform", `translate(${_margin.left}, 0)`)
                .append("svg:title") //now when you hover over the bars, it will tell you which robot it represents
                .text(function(d) {
                return d.health; });
                // same as return d["robot"];
    }

    this.update = function() {
        //remove old data
        _vis1.svg.selectAll("*")
            .remove();    

        //add new data
        _vis1.setupScales([_vis1.height - _margin.bottom, _margin.top], [0, 100], [0, _vis1.width - _margin.left], _vis1.data.length);
        _vis1.setupAxis();
        _vis1.createBars();
    }
}

/* --------------------------------------------------------------------------------------------- */
/* ---------------------------------------- LINE GRAPH ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */
var singleLineGraph = function () {
    this.data;
    this.width = WIDTH;
    this.height = HEIGHT;

    this.svg;
    this.line;

    this.parseTime;
    this.xAxisScale;

    this.xScale;
    this.yScale;

    this.yRange;
    this.yLabel;

    this.xAxis;
    this.yAxis;
    this.gx;

    this.dataNestLength;
    this.legendSpace = {x:70, y:18};

    this.setupScales = function(yRange, yDomain, xRange){
        //kind of like the min and max value of range in last tut
        this.yRange = yRange;

        this.data.forEach(function(d) {
            if (typeof(d.date) === "string") {
              d.date = Date.parse(d.date);
            }
            d.result = +d.result;
        });

        this.yScale = d3.scaleLinear()
            .domain([0, d3.max(this.data, function(d) { return d.result; })])
            .range(yRange);

        this.xScale = d3.scaleTime()
            .domain(d3.extent(this.data, function(d) { return d.date; }))
            .range([_margin.right, this.width - _margin.left - 10]);

        this.xAxisScale = d3.scaleBand()
            .range([0, this.width - _margin.left])
            .domain(this.data.map(function(d){ return d.robot; }));
        
        // x-axis label
        this.svg.append("text")
            .attr("x", this.width / 2)
            .attr("y", this.height - _margin.bottom / 2 + 15)
            .style("text-anchor", "middle")
            .text("Time");

        // y-axis label
        this.svg.append("text")
            .attr("x", _margin.left)
            .attr("y", this.height/2)
            .attr("transform", `rotate(-90, ${_margin.left / 3}, ${this.height/2})`)
            .style("text-anchor", "middle")
            .text(this.yLabel);

    }


    this.createLine = function() {
        var yScale = d3.scaleLinear()
            .domain([0, d3.max(this.data, function(d) { return d.result; })])
            .range(this.yRange);

        var xScale = d3.scaleTime()
            .domain(d3.extent(this.data, function(d) { return d.date; }))
            .range([_margin.right, this.width - _margin.left]);

        var valueline = d3.line()
            .x(function(d) { return xScale(d.date)})
            .y(function(d) { return yScale(d.result)});

        this.svg
                .attr("width", this.width + _margin.left + _margin.right)
                .attr("height", this.height + _margin.top + _margin.bottom)
            .append("g")
                .attr("transform", "translate(" + _margin.left + "," + _margin.top + ")");

        //scale range of data
        // console.log(this.data);

        // Add the valueline path.
        this.svg.append("path")
            .data(this.data)
            .attr("class", "line")
            .attr("d", valueline(this.data))
            .attr("id", function(d) { return d.robot+"-"+d.date; })
            .attr("stroke", "blue")
            .attr("stroke-width", 2)
            .attr("fill", "none")
            .attr("transform", `translate(${_margin.left}, 0)`)
            .append("svg:title")
            .text(function(d) {return d.robot;});

        // Add the Legend
        this.svg.append("rect")
            .data(this.data)
            .attr("x", _margin.left + 5)
            .attr("y", this.height + (_margin.bottom/2) )
            .attr("width", 10)
            .attr("height", 10)
            .style("fill", "blue")
            .on("mouseover", function(d) {
                d3.select("#"+d.robot+"-"+d.date)
                    .attr("stroke-width", 5);
            })
            .on("mouseout", function(d) {
                d3.select("#"+d.robot+"-"+d.date)
                    .attr("stroke-width", 2);
            });
        this.svg.append("text")
            .data(this.data)
            .attr("class", "legend_text")
            .attr("x", _margin.left + 20)  // space legend
            .attr("y", this.height + (_margin.bottom/2)+ 10)
            .attr("class", "legend")    // style the legend
            .style("fill", "blue")
            .on("mouseover", function(d) {
                d3.select("#"+d.robot+"-"+d.date)
                    .attr("stroke-width", 5);
                })
            .on("mouseout", function(d) {
                d3.select("#"+d.robot+"-"+d.date)
                    .attr("stroke-width", 2);
            })
            .text(function(d) {return d.robot; });

        // Add the X Axis
        this.svg.append("g")
            .attr("transform", `translate(${_margin.left}, ${this.height - _margin.bottom})`)
            .call(d3.axisBottom(this.xScale));

        // Add the Y Axis
        this.svg.append("g")
            .attr("transform", `translate(${_margin.left}, 0)`)
            .call(d3.axisLeft(this.yScale));

    }

    this.multiLine = function(lineData, i) {

        this.lineColorScale = d3.scaleOrdinal(d3["schemeSet2"]);

        var yScale = d3.scaleLinear()
            .domain([0, d3.max(this.data, function(d) { return d.result; })])
            .range(this.yRange);

        var xScale = d3.scaleTime()
            .domain(d3.extent(this.data, function(d) { return d.date; }))
            .range([_margin.right, this.width - _margin.left]);

        var valueline = d3.line()
            .x(function(d) { return xScale(d.date)})
            .y(function(d) { return yScale(d.result)});

        this.svg
                .attr("width", this.width + _margin.left + _margin.right)
                .attr("height", this.height + _margin.top + _margin.bottom)
            .append("g")
                .attr("transform", "translate(" + _margin.left + "," + _margin.top + ")");

        //scale range of data
        // console.log(this.data);
        // Add the valueline path.
        this.svg.append("path")
            .data(lineData.values)
            .attr("class", "line")
            .attr("id", function(d) { return d.robot+"-"+d.date; })
            .attr("d", valueline(lineData.values))
            .attr("stroke", colors[i])
            .attr("stroke-width", 2)
            .attr("fill", "none")
            .attr("transform", `translate(${_margin.left}, 0)`)
            .append("svg:title")
            .text(lineData.key);

        // Add the Legend
        var legendMax = parseInt((this.width/1.3)/this.legendSpace.x, 10);
        if (i == 0) var j = 0;
        else j = parseInt((i)/legendMax); 

        var k = i - j * legendMax;
        //console.log(legendMax+" "+i+" "+j+" "+k);
        var rect_x = this.legendSpace.x * (k+1) + 25*k;
        var text_x = (this.legendSpace.x + 25)*(k+1);
        //console.log(rect_x + ", " + text_x);

        this.svg.append("rect")
            .data(lineData.values)
            .attr("x", this.legendSpace.x * (k+1) + 15*k)
            .attr("y", this.height + (_margin.bottom/2) + this.legendSpace.y * j - 5)
            .attr("width", 10)
            .attr("height", 10)
            .style("fill", colors[i])
            .on("mouseover", function(d) {
                d3.select("#"+d.robot+"-"+d.date)
                    .attr("stroke-width", 5);
            })
            .on("mouseout", function(d) {
                d3.select("#"+d.robot+"-"+d.date)
                    .attr("stroke-width", 2);
            });
        this.svg.append("text")
            .data(lineData.values)
            .attr("class", "legend_text")
            .attr("x", (this.legendSpace.x + 15)*(k+1))  // space legend
            .attr("y", this.height + (_margin.bottom/2) + this.legendSpace.y * j + 5)
            .attr("class", "legend")    // style the legend
            .style("fill", "black")
            .on("mouseover", function(d) {
                d3.select("#"+d.robot+"-"+d.date)
                    .attr("stroke-width", 5);
                })
            .on("mouseout", function(d) {
                d3.select("#"+d.robot+"-"+d.date)
                    .attr("stroke-width", 2);
            })
            .text(function(d) {return d.robot; });

    }

    this.update = function(rbt_names, datatype) {
        var all_rbt_obs = []; 
        if (datatype == "current") {
            for (var i = 0; i < rbt_names.length; i++) {
                for (var j = 0; j < CURRENT_DATA.length; j++) {
                    if (rbt_names[i] == CURRENT_DATA[j].robot) {
                        all_rbt_obs.push(CURRENT_DATA[j]);
                    }
                }
            }
        } else if (datatype == "temperature") {
            for (var i = 0; i < rbt_names.length; i++) {
                for (var j = 0; j < TEMPERATURE_DATA.length; j++) {
                    if (rbt_names[i] == TEMPERATURE_DATA[j].robot) {
                        all_rbt_obs.push(TEMPERATURE_DATA[j]);
                    }
                }
            }
        }

        this.data = all_rbt_obs;

        //separate by robot names using dataNest
        var dataNest = d3.nest()
            .key(function(d) {return d.robot;})
            .entries(all_rbt_obs);
        //console.log(dataNest);
        this.dataNestLength = dataNest.length;

        //remove old data
        this.svg.selectAll("*")
            .remove();    
        
        this.setupScales([this.height - _margin.bottom, _margin.top], [0, 100], [0, this.width - _margin.left]);

        // Add the X Axis
        this.svg.append("g")
            .attr("transform", `translate(${_margin.left}, ${this.height - _margin.bottom})`)
            .call(d3.axisBottom(this.xScale));

        // Add the Y Axis
        this.svg.append("g")
            .attr("transform", `translate(${_margin.left}, 0)`)
            .call(d3.axisLeft(this.yScale));
        
        for (var i = 0; i < dataNest.length; i++) {
            this.multiLine(dataNest[i], i);
        }
        /*
        //add new data
        _vis1.setupScales([_vis1.height - _margin.bottom, _margin.top], [0, 100], [0, _vis1.width - _margin.left], _vis1.data.length);
        _vis1.setupAxis();
        _vis1.createBars();
        */
    }
}

/* --------------------------------------------------------------------------------------------- */
/* ----------------------------------- ROBOT DOT CHART ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function setUpVis7() {
    if (th.length > 0) {
        var newData = [];
        for (var i = 0; i < th.length; i++) {
            var name = th[i].name.slice(0,5);
            if (name == "robot") {
                if (th[i].status == "Healthy") var stat = "1 - Healthy";
                else if (th[i].status == "Warning") var stat = "2 - Warning";
                else if (th[i].status == "Urgent") var stat = "3 - Urgent";
                else if (th[i].status == "Unknown") var stat = "4 - Unknown";
                else if (th[i].status == "Needs Parts") var stat = "5 - Needs Parts";
                var entry = {
                    "robot" : th[i].name,
                    "id" : th[i].id,
                    "status" : stat
                };
                newData.push(entry);
            }
        }

        _vis7data = [{
            "name": "robots",
            "values": newData
        }]
        setupDotChart();
    } else {
        setTimeout(setUpVis7, 500)
    }
}

/*
function check_newData() {
    if (newData.length > 0) {
        setup();
    } else {
        setTimeout(check_newData, 500);
    }
}*/

function setupDotChart(){
    vega.scheme('basic', ['#32D144', '#FB7F28', '#EC1C24', '#3F48CC', '#585858', '#000000']);

    var spec = {
    "$schema": "https://vega.github.io/schema/vega/v5.json",
    "width": 1000,
    "height": 200,
    "padding": {"left": 5, "right": 5, "top": 0, "bottom": 20},
    "autosize": "none",

    "signals": [
        { "name": "cx", "update": "width / 2" },
        { "name": "cy", "update": "height / 2" },
        { "name": "radius", "value": 8, "bind": {"input": "range", "min": 2, "max": 15, "step": 1} },
        { "name": "collide", "value": 1},
        { "name": "gravityX", "value": 0.2},
        { "name": "gravityY", "value": 0.1},
        { "name": "static", "value": false}
    ],

    "data": _vis7data,

    "scales": [
        {
        "name": "xscale",
        "type": "band",
        "domain": {
            "data": "robots",
            "field": "status",
            "sort": true
        },
        "range": "width"
        },
        {
        "name": "color",
        "type": "ordinal",
        "domain": {"data": "robots", "field": "status", "sort": true},
        "range": {"scheme": "basic"}
        }
    ],

    "axes": [
        { "orient": "bottom", "scale": "xscale" }
    ],

    "marks": [
        {
        "name": "nodes",
        "type": "symbol",
        "from": {"data": "robots"},
        "encode": {
            "enter": {
            "fill": {"scale": "color", "field": "status"},
            "xfocus": {"scale": "xscale", "field": "status", "band": 0.5},
            "yfocus": {"signal": "cy"}
            },
            "update": {
            "size": {"signal": "pow(2 * radius, 2)"},
            "stroke": {"value": "white"},
            "strokeWidth": {"value": 1},
            "zindex": {"value": 0}
            },
            "hover": {
            "stroke": {"value": "purple"},
            "strokeWidth": {"value": 3},
            "zindex": {"value": 1}
            }
        },
        "transform": [
            {
            "type": "force",
            "iterations": 300,
            "static": {"signal": "static"},
            "forces": [
                {"force": "collide", "iterations": {"signal": "collide"}, "radius": {"signal": "radius"}},
                {"force": "x", "x": "xfocus", "strength": {"signal": "gravityX"}},
                {"force": "y", "y": "yfocus", "strength": {"signal": "gravityY"}}
            ]
            }
        ]
        }
    ]
    }
    console.log("vega done");

    vegaEmbed('#vis7', spec).then(function(result) {
        
        // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
    }).catch(console.error);
}

/* --------------------------------------------------------------------------------------------- */
/* -------------------------------------- SET UP VIS 2 ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function setupVis2(){
    if (CURRENT_DATA.length > 0) {
        _vis2 = new singleLineGraph();
        _vis2.svg = d3.select("#vis2");
        //match size of svg container in html
        _vis2.width = _vis2.svg.node().getBoundingClientRect().width != undefined ?
            _vis2.svg.node().getBoundingClientRect().width : _vis2.width; //if undefined
        _vis2.height = _vis2.svg.node().getBoundingClientRect().height;
        _vis2.yLabel = "Current (Ampere)";

        var temp = msg_vis2.split(" ");
        var rbt_names = [];
        for (var i = 0; i < temp.length; i++) {
            var temp2 = temp[i].split(/\r?\n/);
            rbt_names = rbt_names.concat(temp2);
        }

        //_vis2.data = data2;
        //_vis2.setupScales([_vis2.height - _margin.bottom, _margin.top], [0, 100], [0, _vis2.width - _margin.left]);
        //_vis2.setupAxis();
        _vis2.update(rbt_names, "current");
    } else {
        setTimeout(setupVis2, 500);
    }
}

/* --------------------------------------------------------------------------------------------- */
/* -------------------------------------- SET UP VIS 3 ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function setupVis3(){
    if (TEMPERATURE_DATA.length > 0) {
        _vis3 = new singleLineGraph();
        _vis3.svg = d3.select("#vis3");
        //match size of svg container in html
        _vis3.width = _vis3.svg.node().getBoundingClientRect().width != undefined ?
            _vis3.svg.node().getBoundingClientRect().width : _vis3.width; //if undefined
        _vis3.height = _vis3.svg.node().getBoundingClientRect().height;
        _vis3.yLabel = "Temperature (Celcius)";

        var temp = msg_vis2.split(" ");
        var rbt_names = [];
        for (var i = 0; i < temp.length; i++) {
            var temp2 = temp[i].split(/\r?\n/);
            rbt_names = rbt_names.concat(temp2);
        }

        _vis3.update(rbt_names, "temperature");
    } else {
        setTimeout(setupVis3, 500);
    }
}

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
/* -------------------------------------- SET UP VIS 5 ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

// code modified from Jerome Freye's example @ http://bl.ocks.org/jfreyre/b1882159636cc9e1283a
function setupVis5(){
    if (TEMPERATURE_DATA.length > 0) {
        _vis5 = new singleLineGraph();
        _vis5.svg = d3.select("#vis5");
        //match size of svg container in html
        _vis5.width = _vis5.svg.node().getBoundingClientRect().width != undefined ?
            _vis5.svg.node().getBoundingClientRect().width : _vis5.width; //if undefined
        _vis5.height = _vis5.svg.node().getBoundingClientRect().height;

        var data3 = [];
        var count = 0;

        for (let i = 0; i < TEMPERATURE_DATA.length; i++) {
            if (TEMPERATURE_DATA[i].robot === "robot1") {
                // console.log(TEMPERATURE_DATA[i].robot);
                data3.push(TEMPERATURE_DATA[i]);
                count++;
            }
        }

        _vis5.data = data3;
        _vis5.setupScales([_vis5.height - _margin.bottom, _margin.top], [0, 100], [0, _vis5.width - _margin.left], _vis5.data.length);
        //_vis2.setupAxis();
        _vis5.createLine();
    } else {
        setTimeout(setupVis5, 500);
    }
    
}

/* --------------------------------------------------------------------------------------------- */
/* -------------------------------------- SET UP VIS 6 ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function setupVis6(){
    if (TEMPERATURE_DATA.length > 0) {
        _vis6 = new singleLineGraph();
        _vis6.svg = d3.select("#vis6");
        //match size of svg container in html
        _vis6.width = _vis6.svg.node().getBoundingClientRect().width != undefined ?
            _vis6.svg.node().getBoundingClientRect().width : _vis6.width; //if undefined
        _vis6.height = _vis6.svg.node().getBoundingClientRect().height;

        var data3 = [];
        var count = 0;

        for (let i = 0; i < TEMPERATURE_DATA.length; i++) {
            if (TEMPERATURE_DATA[i].robot === "robot2") {
                // console.log(TEMPERATURE_DATA[i].robot);
                data3.push(TEMPERATURE_DATA[i]);
                count++;
            }
        }

        _vis6.data = data3;
        _vis6.setupScales([_vis6.height - _margin.bottom, _margin.top], [0, 100], [0, _vis6.width - _margin.left], _vis6.data.length);
        //_vis2.setupAxis();
        _vis6.createLine();
    } else {
        setTimeout(setupVis6, 500);
    }
}

/* --------------------------------------------------------------------------------------------- */
/* -------------------------------------------- EXPORT ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

export default {
  name: 'Analytics',
  mounted () {
    getData();
    setupVis1();
    setupVis2();
    setupVis3();
    setupVis4();
    setupVis5();
    setupVis6();
    setUpVis7();  
  },
  data () {
    return {
      msg: '',
      _data1: this._data1,
      _vis_height: this._vis_height,
      _vis_width: this._vis_width,
      PADDING_FOR_LABELS: this.PADDING_FOR_LABELS,
      message_v2: "robot1\nrobot2\nrobot3\nrobot4",
      message_v3: "robot1\nrobot2\nrobot3\nrobot4"
    }
  },
  methods: {
        changeHealthBarHeights(attr, maxAttrValue) {
            for (var i = 0; i < _data1.length; i++){
                var newHeight = mapValue(_data1[i][attr], 0, maxAttrValue, 0, _vis_height - PADDING_FOR_LABELS);
                var bar = document.getElementById("column_" + i);

                var oldY = bar.getAttribute("y");
                var oldHeight = bar.getAttribute("height");
                var newY = _vis_height - PADDING_FOR_LABELS - newHeight;

                bar.setAttribute("y", oldY);
                bar.setAttribute("height", oldHeight);

                var animate = "<animate id='animate_bar_" + i + "' attributeName='y' from='" + oldY + "' " +
                    "to='" + newY + "' dur='1s' begin='indefinite'" +
                    "repeatCount='1' fill='freeze'></animate>" +
                    "<animate attributeName='height' from='"+ oldHeight +"' to='"+ newHeight +"' dur='1s' " +
                    "begin='animate_bar_"+ i +".begin' fill='freeze'></animate>" +
                    "<title>"+ _data1[i][attr] +"</title>";
                bar.innerHTML = animate;
                document.getElementById('animate_bar_' + i).beginElement();
            }
        },
        vis1_switch(order) {
            if (order === "name-ascending") {
                _vis1.data.sort((a, b) => d3.ascending(parseInt(a.robot.slice(1),10), parseInt(b.robot.slice(1),10)));
            }
            if (order === "value-ascending") {
                _vis1.data.sort((a, b) => a.health - b.health);
            }
            if (order === "value-descending") {
                _vis1.data.sort((a, b) => b.health - a.health);
                console.log(_vis1.data);
            }
            _vis1.xAxisScale.domain(_vis1.data.map(d => d.name));
            _vis1.update();
        },
        vis2_update() {
            var temp = this.message_v2.split(" ");
            var rbt_names = [];
            for (var i = 0; i < temp.length; i++) {
                var temp2 = temp[i].split(/\r?\n/);
                rbt_names = rbt_names.concat(temp2);
            }
            //console.log(rbt_names);
            _vis2.update(rbt_names, "current");
        },
        vis3_update() {
            var temp = this.message_v3.split(" ");
            var rbt_names = [];
            for (var i = 0; i < temp.length; i++) {
                var temp2 = temp[i].split(/\r?\n/);
                rbt_names = rbt_names.concat(temp2);
            }
            //console.log(rbt_names);
            _vis3.update(rbt_names, "temperature");
        }
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

div#vis1box {
    overflow-y: scroll;
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

#vis2box {
    overflow-x:hidden;
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

#vis4 {
    background: white;
    display: block;
    width: 90%;
    height: 100%;
    min-width: 800px;
    min-height: 300px;
    box-sizing: border-box;
    margin: 10px auto;
    padding: 25px;
}

#vis4 div {
    width: 60px;
    height: 60px;
    float: left;
    margin: 1px;
}
#vis2textbox {
    min-height: 300px;
}
#vis3textbox {
    min-height: 300px;
}

#vis1box {
    min-height: 600px;
}

#vis2box {
    min-height: 600px;
}
#vis3box {
    min-height: 600px;
}

#vis7 {
    height: 300px;
    width: 100%;
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
