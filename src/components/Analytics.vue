/* eslint-disable */
<template>
        <div id="div_visuals">
            <h3 class="head">Robot Health</h3>
            <div id="vis1box" class="vis_div">
                <svg id="vis1" class="svg_boxes"></svg>
            </div>
            <div id="vis1btn" class="vis_btn">
                <button id="btn_name_ascending" class="cat" v-on:click="vis1_switch('name-ascending')">Name Ascending</button>
                <button id="btn_val_ascending" class="cat" v-on:click="vis1_switch('value-ascending')">Value Ascending</button>
                <button id="btn_val_descending" class="cat" v-on:click="vis1_switch('value-descending')">Value Descending</button>
            </div>
            <div class="spacer"></div>
            <h3>Barometer_123: Robot_1</h3>
            <div id="vis2box" class="vis_div">
                <svg id="vis2" class="svg_boxes"></svg>
            </div>
            <div id="vis2btn" class="vis_btn">
                <p>Enter robot names: </p>
                <textarea id="vis2textbox" v-model="message" placeholder="add multiple lines"></textarea>
                <br>
                <button id="btn_vis2_update" class="cat" v-on:click="vis2_update()">Update Chart</button>
                <p style="white-space: pre-line;">{{ message }}</p>
            </div>
          <h3>Barometer_123: Robot_2</h3>
          <svg id="vis3" class="svg_boxes"></svg>
          <h3>Thermometer_236: Robot_1</h3>
          <svg id="vis5" class="svg_boxes"></svg>
          <h3>Thermometer_236: Robot_2</h3>
          <svg id="vis6" class="svg_boxes"></svg>
          <h3>Historical Data</h3>
          <svg id="vis4" class="svg_boxes"></svg>
      </div>
</template>

<script>
import * as d3 from 'd3'

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
const PRESSURE_DATA = [
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:05.000Z", "result" : 30 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:06.000Z", "result" : 40 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:07.000Z", "result" : 20 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:08.000Z", "result" : 10 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:09.000Z", "result" : 30 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:10.000Z", "result" : 60 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:11.000Z", "result" : 50 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:12.000Z", "result" : 80 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:13.000Z", "result" : 20 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:14.000Z", "result" : 10 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:05.000Z", "result" : 40 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:06.000Z", "result" : 60 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:07.000Z", "result" : 20 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:08.000Z", "result" : 80 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:09.000Z", "result" : 10 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:10.000Z", "result" : 50 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:11.000Z", "result" : 30 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:12.000Z", "result" : 20 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:13.000Z", "result" : 60 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:14.000Z", "result" : 40 },
]


var TEMPERATURE_DATA = [];
/*[
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:05.000Z", "result" : 30 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:06.000Z", "result" : 33 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:07.000Z", "result" : 35 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:08.000Z", "result" : 37 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:09.000Z", "result" : 32 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:10.000Z", "result" : 30 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:11.000Z", "result" : 33 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:12.000Z", "result" : 29 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:13.000Z", "result" : 34 },
    { "robot" : "robot_1", "date" : "2019-02-07T18:02:14.000Z", "result" : 35 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:05.000Z", "result" : 40 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:06.000Z", "result" : 39 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:07.000Z", "result" : 38 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:08.000Z", "result" : 35 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:09.000Z", "result" : 32 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:10.000Z", "result" : 30 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:11.000Z", "result" : 31 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:12.000Z", "result" : 29 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:13.000Z", "result" : 30 },
    { "robot" : "robot_2", "date" : "2019-02-07T18:02:14.000Z", "result" : 32 },
]*/

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
var parseTime = d3.timeParse("%H:%M %p");
var parseDate = d3.timeParse("%Y-%m-%d");
//var data = [10, 20, 30 , 40, 50];
var th;

var HPyRange;
var HPyDomain;
var HPxRange;
var HPxLength;


/* --------------------------------------------------------------------------------------------- */
/* ------------------------------------ LOAD DATA FROM API ------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function loadObservation(obid){
    //create object to hold observation id, result, and time
    var obj_obs = function(id, result, time) {
        this.id = id;
        this.result = result;
        this.time = time;
    }
    //create an object with null values to hold resulting obs
    var obs = new obj_obs(null, null, null);
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var r = JSON.parse(xhttp.responseText);

            obs.id = r['@iot.id'];
            obs.result = r['result'];
            obs.time = r['resultTime'];
        }
    };
    xhttp.open("GET", "http://routescout.sensorup.com/v1.0/Observations("+obid+")", true);
    xhttp.send();
    return obs;
}

function loadDatastreams_Obs(){
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
                    var obs_info = loadObservation(obid);

                    //push to obids, which now contains obs info (id, result, time)
                    obids.push(obs_info);
                }

                //create new obj_ds_ob to hold all of the data
                var dsob = new Obj_ds_ob(dsid,type,obids);
                //add to array of datastream w obs
                dsobs.push(dsob);
            }
        }
    };
    xhttp.open("GET", "http://routescout.sensorup.com/v1.0/Datastreams?$expand=Observations", true);
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
                /*
                for (var m = 0; m < thds.length; m++) {
                    if (thds[m].type = 'T') {
                        thdsob.dsT = thds[m];
                    } else if (thds[m].type = 'P') {
                        thdsob.dsP = thds[m];
                    } else if (thds[m].type = 'H') {
                        thdsob.dsH = thds[m];
                    }
                }
                */
                //append to final list of all things
                thdsobs.push(thdsob);
            }
        }
    };
    xhttp.open("GET", "http://routescout.sensorup.com/v1.0/Things?$expand=Datastreams", true);
    xhttp.send();
    return thdsobs;
}

function getData(){
    var ds = loadDatastreams_Obs();
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
            //console.log(th[5].ds[1].id);
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
            .range([0, this.width - _margin.left])
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

    this.xAxis;
    this.yAxis;
    this.gx;

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
            .attr("class", "line")
            .attr("d", valueline(this.data))
            .attr("stroke", "blue")
            .attr("stroke-width", 2)
            .attr("fill", "none")
            .attr("transform", `translate(${_margin.left}, 0)`)
            .append("svg:title");

        // Add the X Axis
        this.svg.append("g")
            .attr("transform", `translate(${_margin.left}, ${this.height - _margin.bottom})`)
            .call(d3.axisBottom(this.xScale));

        // Add the Y Axis
        this.svg.append("g")
            .attr("transform", `translate(${_margin.left}, 0)`)
            .call(d3.axisLeft(this.yScale));

    }

    function drawLine(lineData,lineColor,lineLabel,lineId)
    {
            // append line to svg
        var group = this.svg.append("g")
                        .attr('class', lineId);

            group.append("svg:path")
                    .attr('d', lineSelection(lineData))
                    .attr('stroke', lineColor)
                    .attr('stroke-width', 2)
                    .attr('fill', 'none');

        // prepare label for line
        group.append("rect")
            .attr("width", chartConfig.lineLabel.width)
            .attr("height", chartConfig.lineLabel.height)
            .attr("x", xScale(lineData[0].year)-100)
            .attr("y", yScale(lineData[0].sale)-
            (chartConfig.lineLabel.height/2))
            .attr("stroke", lineColor)
            .attr("fill", lineColor)
            .attr("stroke-width", 1);

    // draw line label text
    group.append("text")
            .attr("dx", xScale(lineData[0].year)-(chartConfig.lineConnectorLength+7))
        .attr("dy", yScale(lineData[0].sale)+4) // 4 is padding
            .attr("text-anchor", "end")
        .attr("class", "lineLabel")
            .style("fill", "white")
            .text(lineLabel);

    // line to label connector
    group.append("line")
    .attr({
    x1: xScale(lineData[0].year), y1: yScale(lineData[0].sale), //start of the line
    x2: xScale(lineData[0].year)-chartConfig.lineConnectorLength, y2: yScale(lineData[0].sale)  //end of the line
            })
    .attr('stroke', lineColor)
    .attr('stroke-width', 2)
    .attr('fill', lineColor);

    return group;
    }
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

        var data2 = [];
        var count = 0;

        for (let i = 0; i < CURRENT_DATA.length; i++) {
            if (CURRENT_DATA[i].robot === "robot1") {
                //console.log(PRESSURE_DATA[i].robot);
                data2.push(CURRENT_DATA[i]);
                count++;
            }
        }

        _vis2.data = data2;
        _vis2.setupScales([_vis2.height - _margin.bottom, _margin.top], [0, 100], [0, _vis2.width - _margin.left], _vis2.data.length);
        //_vis2.setupAxis();
        _vis2.createLine();
    } else {
        setTimeout(setupVis2, 500);
    }
}

/* --------------------------------------------------------------------------------------------- */
/* -------------------------------------- SET UP VIS 3 ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function setupVis3(){
    if (CURRENT_DATA.length > 0) {
        _vis3 = new singleLineGraph();
        _vis3.svg = d3.select("#vis3");
        //match size of svg container in html
        _vis3.width = _vis3.svg.node().getBoundingClientRect().width != undefined ?
            _vis3.svg.node().getBoundingClientRect().width : _vis3.width; //if undefined
        _vis3.height = _vis3.svg.node().getBoundingClientRect().height;

        var data3 = [];
        var count = 0;

        for (let i = 0; i < CURRENT_DATA.length; i++) {
            if (CURRENT_DATA[i].robot === "robot2") {
                //console.log(PRESSURE_DATA[i].robot);
                data3.push(CURRENT_DATA[i]);
                count++;
            }
        }

        _vis3.data = data3;
        _vis3.setupScales([_vis3.height - _margin.bottom, _margin.top], [0, 100], [0, _vis3.width - _margin.left], _vis3.data.length);
        //_vis2.setupAxis();
        _vis3.createLine();
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
        console.log(data3);
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
  },
  data () {
    return {
      msg: '',
      _data1: this._data1,
      _vis_height: this._vis_height,
      _vis_width: this._vis_width,
      PADDING_FOR_LABELS: this.PADDING_FOR_LABELS,
      message: null
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
            var temp = this.message.split(" ");
            var rbt_names = [];
            for (var i = 0; i < temp.length; i++) {
                var temp2 = temp[i].split(/\r?\n/);
                rbt_names = rbt_names.concat(temp2);
            }
            console.log(rbt_names);
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
    overflow:scroll;
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
    height: 430px;
    overflow-y: scroll;
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
    min-height: 200px;
}

.spacer {
    height: 200px;
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
