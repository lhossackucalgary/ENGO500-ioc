/* eslint-disable */
<template>
  <div class="">
  <div id="div_visuals">
    <h2>Compare Robots Page</h2>
    <p>{{$store.state.selected_items}}</p>
        <div>
            <div id="vis1box" class="vis_div visbox">
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
var COMP_ROBOT_HEALTH = [];
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
/* ------------------------------------- HEALTH BAR CHART -------------------------------------- */
/* --------------------------------------------------------------------------------------------- */


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
        // Add the valueline path.
        this.svg.append("path")
            .data(lineData.values)
            .attr("class", "line")
            .attr("id", function(d) { 
                return d.robot+"-"+d.date; 
                })
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
/* --------------------------------------------------------------------------------------------- */
/* ------------------------------ API DATA TO OBSERVATION DATA --------------------------------- */
/* --------------------------------------------------------------------------------------------- */
    saveCompBots() {
      compBots = this.$store.state.selected_items;
    },
    saveData() {
        //extract latest health observation
        //{ "robot" : "robot_1", "health" : 90, "pressure" : 40, "temperature" : 20}
        if (this.$store.state.th.length > 0) {
            COMP_ROBOT_HEALTH = [];
            var th = this.$store.state.th;
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
                            COMP_ROBOT_HEALTH.push(rh_obs);
                        }
                    }
                }
            });
            }
            compBots = [];
        } else {
            setTimeout(this.saveData(), 500);
        }
    },
/* --------------------------------------------------------------------------------------------- */
/* -------------------------------------- SET UP VIS'S ----------------------------------------- */
/* --------------------------------------------------------------------------------------------- */
    setupVis1() {
        if (COMP_ROBOT_HEALTH.length > 0) {
            _vis1 = new Healthplot();
            _vis1.svg = d3.select("#vis1");
            //match size of svg container in html
            _vis1.width = _vis1.svg.node().getBoundingClientRect().width != undefined ?
                _vis1.svg.node().getBoundingClientRect().width : _vis1.width; //if undefined
            _vis1.height = _vis1.svg.node().getBoundingClientRect().height;

            _vis1.data = COMP_ROBOT_HEALTH;
            _vis1.setupScales([_vis1.height - _margin.bottom, _margin.top], [0, 100], [0, _vis1.width - _margin.left], _vis1.data.length);
            _vis1.setupAxis();
            _vis1.createBars();
        } else {
            setTimeout(this.setupVis1, 500);
        }
    },
    setupVis2() {
        if (this.$store.state.CURRENT_DATA.length > 0 && COMP_ROBOT_HEALTH.length > 0) {
            CURRENT_DATA = this.$store.state.CURRENT_DATA;
            _vis2 = new singleLineGraph();
            _vis2.svg = d3.select("#vis2");

            //match size of svg container in html
            _vis2.width = _vis2.svg.node().getBoundingClientRect().width != undefined ?
                _vis2.svg.node().getBoundingClientRect().width : _vis2.width; //if undefined
            _vis2.height = _vis2.svg.node().getBoundingClientRect().height;
            _vis2.yLabel = "Current (Ampere)";

            var rbt_names = [];
            message_v2 = "";
            COMP_ROBOT_HEALTH.forEach(ob => {
                rbt_names.push(ob.robot);
                message_v2 = message_v2.concat(ob.robot+"\n");
            })
            
            _vis2.update(rbt_names, "current");

        } else {
            setTimeout(this.setupVis2, 500);
        }
    },
    setupVis3() {
        if (this.$store.state.TEMPERATURE_DATA.length > 0 && COMP_ROBOT_HEALTH.length > 0) {
            TEMPERATURE_DATA = this.$store.state.TEMPERATURE_DATA;
            _vis3 = new singleLineGraph();
            _vis3.svg = d3.select("#vis3");
            //match size of svg container in html
            _vis3.width = _vis3.svg.node().getBoundingClientRect().width != undefined ?
                _vis3.svg.node().getBoundingClientRect().width : _vis3.width; //if undefined
            _vis3.height = _vis3.svg.node().getBoundingClientRect().height;
            _vis3.yLabel = "Temperature (Celcius)";

            var rbt_names = [];
            message_v3 = "";
            COMP_ROBOT_HEALTH.forEach(ob => {
            rbt_names.push(ob.robot);
            message_v3 = message_v3.concat(ob.robot+"\n");
            })
            _vis3.update(rbt_names, "temperature");
        } else {
            setTimeout(this.setupVis3, 500);
        }
    },
    setupVis4() {
        if (this.$store.state.ALL_ROBOT_HEALTH.length > 0 && COMP_ROBOT_HEALTH.length > 0) {
            ALL_ROBOT_HEALTH = this.$store.state.ALL_ROBOT_HEALTH;
            _vis4 = new singleLineGraph();
            _vis4.svg = d3.select("#vis4");
            //match size of svg container in html
            _vis4.width = _vis4.svg.node().getBoundingClientRect().width != undefined ?
                _vis4.svg.node().getBoundingClientRect().width : _vis4.width; //if undefined
            _vis4.height = _vis4.svg.node().getBoundingClientRect().height;
            _vis4.yLabel = "Health (%)";

            var rbt_names = [];
            message_v4 = "";
            COMP_ROBOT_HEALTH.forEach(ob => {
            rbt_names.push(ob.robot);
            message_v4 = message_v4.concat(ob.robot+"\n");
            })
            
            _vis4.update(rbt_names, "health");
        } else {
            setTimeout(this.setupVis4, 500);
        }
    },
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
        _vis2.update(rbt_names, "current");
    },
    vis3_update() {
        var temp = this.message_v3.split(" ");
        var rbt_names = [];
        for (var i = 0; i < temp.length; i++) {
            var temp2 = temp[i].split(/\r?\n/);
            rbt_names = rbt_names.concat(temp2);
        }
        _vis3.update(rbt_names, "temperature");
    },
    vis4_update() {
        var temp = this.message_v4.split(" ");
        var rbt_names = [];
        for (var i = 0; i < temp.length; i++) {
            var temp2 = temp[i].split(/\r?\n/);
            rbt_names = rbt_names.concat(temp2);
        }
        _vis4.update(rbt_names, "health");
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
    this.saveData();
    this.setupVis1();
    this.setupVis2();
    this.setupVis3();
    this.setupVis4();
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
    overflow: hidden;
}
.spacer {
    height: 100px;
    float: left;
    width: 100%;
}
</style>
