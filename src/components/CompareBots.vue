/* eslint-disable */
<template>
  <div class="">
  <div id="div_visuals">
    <h2>Compare Robots Page</h2>
    <p>{{$store.state.selected_items}}</p>
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
            <div class="vis_div visbox">
                <h3>Robot Health History</h3>
                <svg id="vis4" class="svg_boxes"></svg>
            </div>
            <div id="vis4btn" class="vis_btn">
                <p>Enter list of robot names: </p>
                <textarea class="vistextbox" v-model="message_v4" placeholder="robot1 robot2 ..."></textarea>
                <br>
                <button id="btn_vis4_update" class="cat" v-on:click="vis4_update()">Update Chart</button>
            </div>
        </div>
        <div class="spacer"></div>
        <div>
            <div class="vis_div visbox">
                <h3>Sensor807: Motor Power Draw</h3>
                <svg id="vis2" class="svg_boxes"></svg>
            </div>
            <div id="vis2btn" class="vis_btn">
                <p>Enter list of robot names: </p>
                <textarea class="vistextbox" v-model="message_v2" placeholder="robot1 robot2 ..."></textarea>
                <br>
                <button id="btn_vis2_update" class="cat" v-on:click="vis2_update()">Update Chart</button>
            </div>
        </div>
        <div class="spacer"></div>
        <div>
            <div class="vis_div visbox">
                <h3>Sensor876: CPU Temperature</h3>
                <svg id="vis3" class="svg_boxes"></svg>
            </div>
            <div id="vis3btn" class="vis_btn">
                <p>Enter list of robot names: </p>
                <textarea class="vistextbox" v-model="message_v3" placeholder="robot1 robot2 ..."></textarea>
                <br>
                <button id="btn_vis3_update" class="cat" v-on:click="vis3_update()">Update Chart</button>
            </div>
        </div>
        <div class="spacer"></div>
      </div>

  </div>
</template>

<script>
import * as d3 from 'd3'

var th;
var compBots;
var ROBOT_HEALTH = [];
var ALL_ROBOT_HEALTH = [];
var TEMPERATURE_DATA = [];
var CURRENT_DATA = [];
var message_v2;
var message_v3;
var message_v4;

const _margin = ({top: 10, right: 0, bottom: 30, left: 40});
var parseTime = d3.timeParse("%H:%M %p");
var parseDate = d3.timeParse("%Y-%m-%d");
var colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#fabebe', '#008080', '#e6beff', '#9a6324', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080',
    '#806060', '#ff2200', '#330e00', '#e59173', '#993d00', '#4d4139', '#d97400', '#f2ba79', '#d9bfa3', '#ffaa00', '#734d00', '#332200', '#bfb300', '#6f7339', '#ccff00', '#1b3300', '#639926', '#d9ffbf', '#3df23d', '#304030', '#00733d', '#00f2a2',
    '#2db3aa', '#005c73', '#40d9ff', '#8fb6bf', '#002233', '#003d73', '#3995e6', '#001180', '#070033', '#574d99', '#7e39e6', '#3b264d', '#6b0073', '#b086b3', '#f23de6', '#b2005f', '#33001b', '#73002e', '#f27999', '#b20018']; // '#ffffff', '#000000',

var _vis1;
var _vis2;
var _vis3;
var _vis4;

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

function saveData() {
    //extract latest health observation
    //{ "robot" : "robot_1", "health" : 90, "pressure" : 40, "temperature" : 20}
    ALL_ROBOT_HEALTH = [];
    ROBOT_HEALTH = [];
    var obj_rb = function(robot, date, health) {
        this.robot = robot;
        this.date = date;
        this.result = health;
    }
    for (var i = 0; i < th.length; i++) {
      compBots.forEach(cid => {
        if (cid == th[i].id) {
          var ds = th[i].ds;
            var health = null;
            var rname = th[i].name;
            for (var j = 0; j < ds.length; j++) {
              if (ds[j].type == 'H') {
                health = ds[j].obids[0].result;
                var rh_obs = new obj_rb(rname, ds[j].obids[0].time, health);
                ROBOT_HEALTH.push(rh_obs);
                ds[j].obids.forEach(ob => {
                  result = ob.result;
                  date = ob.time;
                  var h_obs = new obj_rb(rname, date, result);
                  ALL_ROBOT_HEALTH.push(h_obs);
                });
              }
            }
        }
      });
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
    this.width;
    this.height;

    this.svg;
    this.bar;

    this.xAxisScale;
    this.xScale;
    this.yScale;

    this.xAxis;
    this.yAxis;
    this.gx;

    this.setupScales = function(yRange, yDomain, xRange, xLength){

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
                .attr("height", function(d) { return (_vis1.height - _margin.bottom - _vis1.yScale(d.result)); })
                .attr("x", function(d, i) { return _vis1.xScale(i); })
                .attr("y", function(d) { return _vis1.yScale(d.result); })
                .attr("transform", `translate(${_margin.left}, 0)`)
                .append("svg:title") //now when you hover over the bars, it will tell you which robot it represents
                .text(function(d) {
                return d.result; });
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
    this.width;
    this.height;

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
        } else if (datatype == "health") {
            for (var i = 0; i < rbt_names.length; i++) {
                for (var j = 0; j < ALL_ROBOT_HEALTH.length; j++) {
                    if (rbt_names[i] == ALL_ROBOT_HEALTH[j].robot) {
                        all_rbt_obs.push(ALL_ROBOT_HEALTH[j]);
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
/* -------------------------------------- SET UP VIS 2 ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function setupVis2(){
    if (CURRENT_DATA.length > 0) {
        _vis2 = new singleLineGraph();
        _vis2.svg = d3.select("#vis2");
        console.log(_vis2.svg);
        //match size of svg container in html
        _vis2.width = _vis2.svg.node().getBoundingClientRect().width != undefined ?
            _vis2.svg.node().getBoundingClientRect().width : _vis2.width; //if undefined
        _vis2.height = _vis2.svg.node().getBoundingClientRect().height;
        _vis2.yLabel = "Current (Ampere)";

        var rbt_names = [];
        message_v2 = "";
        ROBOT_HEALTH.forEach(ob => {
          rbt_names.push(ob.robot);
          message_v2 = message_v2.concat(ob.robot+"\n");
        })
        
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

        var rbt_names = [];
        message_v3 = "";
        ROBOT_HEALTH.forEach(ob => {
          rbt_names.push(ob.robot);
          message_v3 = message_v3.concat(ob.robot+"\n");
        })

        _vis3.update(rbt_names, "temperature");
    } else {
        setTimeout(setupVis3, 500);
    }
}

/* --------------------------------------------------------------------------------------------- */
/* -------------------------------------- SET UP VIS 4 ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */

function setupVis4(){
    if (ALL_ROBOT_HEALTH.length > 0) {
        _vis4 = new singleLineGraph();
        _vis4.svg = d3.select("#vis4");
        //match size of svg container in html
        _vis4.width = _vis4.svg.node().getBoundingClientRect().width != undefined ?
            _vis4.svg.node().getBoundingClientRect().width : _vis4.width; //if undefined
        _vis4.height = _vis4.svg.node().getBoundingClientRect().height;
        _vis4.yLabel = "Health (%)";

        var rbt_names = [];
        message_v4 = "";
        ROBOT_HEALTH.forEach(ob => {
          rbt_names.push(ob.robot);
          message_v4 = message_v4.concat(ob.robot+"\n");
        })

        _vis4.update(rbt_names, "health");
    } else {
        setTimeout(setupVis4, 500);
    }
}

export default {
  name: 'CompareBots',
  data () {
    return {
      message_v2: this.message_v2,
      message_v3: this.message_v3,
      message_v4: this.message_v4

    }
  },
  methods: {
    vis1_switch(order) {
        if (order === "name-ascending") {
            _vis1.data.sort((a, b) => d3.ascending(parseInt(a.robot.slice(5),10), parseInt(b.robot.slice(5),10)));
        }
        if (order === "value-ascending") {
            _vis1.data.sort((a, b) => a.result - b.result);
        }
        if (order === "value-descending") {
            _vis1.data.sort((a, b) => b.result - a.result);
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
    },
    vis4_update() {
        var temp = this.message_v4.split(" ");
        var rbt_names = [];
        for (var i = 0; i < temp.length; i++) {
            var temp2 = temp[i].split(/\r?\n/);
            rbt_names = rbt_names.concat(temp2);
        }
        console.log(rbt_names);
        _vis4.update(rbt_names, "health");
    },
    saveCompBots() {
      compBots = this.$store.state.selected_items;
    },
    printBotsInTB2() {
      if (message_v2 != undefined) {
        this.message_v2 = message_v2;
      } else {
        setTimeout(this.printBotsInTB2);
      }
    },
    printBotsInTB3() {
      if (message_v3 != undefined) {
        this.message_v3 = message_v3;
      } else {
        setTimeout(this.printBotsInTB3);
      }
    },
    printBotsInTB4() {
      if (message_v4 != undefined) {
        this.message_v4 = message_v4;
      } else {
        setTimeout(this.printBotsInTB4);
      }
    }
  },
  mounted () {
    console.log(this.$store.state.selected_items);
    this.saveCompBots();
    getData();
    setupVis1();
    setupVis2();
    setupVis3();
    setupVis4();
    this.printBotsInTB2();
    this.printBotsInTB3();
    this.printBotsInTB4();
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
.vistextbox {
    min-height: 300px;
}
.visbox {
    min-height: 600px;
}
.spacer {
    height: 100px;
    float: left;
    width: 100%;
}
</style>
