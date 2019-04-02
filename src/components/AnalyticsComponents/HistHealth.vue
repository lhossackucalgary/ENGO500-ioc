<template>
  <div>
      <h2>Robot Health</h2>
      <div id="vis3box" class="vis_div">
          <svg id="vis3" class="svg_boxes"></svg>
      </div>
      <div id="vis3btn" class="vis_btn">
          <p>Enter list of robot names: </p>
          <textarea id="vis3textbox" v-model="message" placeholder="robot1 robot2 ..."></textarea>
          <br>
          <button id="btn_vis3_update" class="cat" v-on:click="vis3_update()">Update Chart</button>
          <div id="tooltipbox"></div>
      </div>
  </div>

</template>

<script>
import * as d3 from 'd3'

const _margin = ({top: 10, right: 0, bottom: 30, left: 40});

var parseTime = d3.timeParse("%H:%M %p");
var parseDate = d3.timeParse("%Y-%m-%d");
var colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#fabebe', '#008080', '#e6beff', '#9a6324', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080',
    '#806060', '#ff2200', '#330e00', '#e59173', '#993d00', '#4d4139', '#d97400', '#f2ba79', '#d9bfa3', '#ffaa00', '#734d00', '#332200', '#bfb300', '#6f7339', '#ccff00', '#1b3300', '#639926', '#d9ffbf', '#3df23d', '#304030', '#00733d', '#00f2a2',
    '#2db3aa', '#005c73', '#40d9ff', '#8fb6bf', '#002233', '#003d73', '#3995e6', '#001180', '#070033', '#574d99', '#7e39e6', '#3b264d', '#6b0073', '#b086b3', '#f23de6', '#b2005f', '#33001b', '#73002e', '#f27999', '#b20018']; // '#ffffff', '#000000',

var month = [
    "January", "February", "March",
    "April", "May", "June", "July",
    "August", "September", "October",
    "November", "December"
  ];

var second = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
    "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
    "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
    "51", "52", "53", "54", "55", "56", "57", "58", "59", "60",
    ];

var _vis3;
var ALL_ROBOT_HEALTH = [];

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

        // Add points with tooltip
        var tooltip = d3.select("#tooltipbox")
                  .attr("class", "tooltip")
                  .style("opacity", 0);

        this.svg.selectAll("#dot"+lineData.values[0].robot)
            .data(lineData.values)
            .enter().append("circle")
            .attr("id", function(d) {return "dot"+d.robot;})
            .attr("r", 4)
            .attr("cx", function(d) { return xScale(d.date);})
            .attr("cy", function(d) { return yScale(d.result);})
            .attr("fill", colors[i])
            .attr("transform", `translate(${_margin.left}, 0)`)
            .on("mouseover", function(d) {
                var color = colors[i];
                var dt = new Date(d.date);
                var timestr = dt.getHours()+":"+dt.getMinutes()+":"+second[dt.getSeconds()];
                var datestr = month[dt.getMonth()]+" "+dt.getDate()+" 20"+(dt.getYear()-100);
                //console.log(fulldt);
                var html  = timestr + "<br/>" + datestr + "<br/>" +
                            "<span style='color:" + color + ";'>" + d.robot + "</span><br/>" +
                            "<b>" + d.result + "</b> %";
                //console.log(d3.event.pageX+" "+d3.event.pageY);
                tooltip.html(html)
                    .style("left", d3.event.pageX + "px")
                    .style("top", d3.event.pageY - 120 + "px")
                .transition()
                    .duration(200) // ms
                    .style("opacity", .9) // started as 0!
            
            })
            .on("mouseout", function(d) {
                tooltip.transition()
                    .duration(300) // ms
                    .style("opacity", 0);
            });

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
            .call(d3.axisBottom(this.xScale).tickFormat(d3.timeFormat("%b %d %H:%M:%S")));

        // Add the Y Axis
        this.yAxis = d3.axisLeft(this.yScale)
            .tickSize(-this.width)
            .tickFormat("");

        this.svg.append("g")
            .attr("transform", `translate(${_margin.left}, 0)`)
            .attr("class","grid")
            .style("opacity", "0.2")
            .call(this.yAxis);
        
        this.svg.append("g")
            .attr("transform", `translate(${_margin.left}, 0)`)
            .call(d3.axisLeft(this.yScale));

        for (var i = 0; i < dataNest.length; i++) {
            this.multiLine(dataNest[i], i);
        }
    }
}

export default {
  name: 'HistHealth',
  data () {
    return {
      _vis3: this._vis3,
      message: "robot1\nrobot2\nrobot3\nrobot4"
    }
  },
  methods: {
    setupVis3(){
      if (this.$store.state.ALL_ROBOT_HEALTH.length > 0) {
          ALL_ROBOT_HEALTH = this.$store.state.ALL_ROBOT_HEALTH;
          this._vis3 = new singleLineGraph();
          this._vis3.svg = d3.select("#vis3");
          //match size of svg container in html
          this._vis3.width = this._vis3.svg.node().getBoundingClientRect().width != undefined ?
              this._vis3.svg.node().getBoundingClientRect().width : this._vis3.width; //if undefined
          this._vis3.height = this._vis3.svg.node().getBoundingClientRect().height;
          this._vis3.yLabel = "Health (%)";

          var temp = this.message.split(" ");
          var rbt_names = [];
          for (var i = 0; i < temp.length; i++) {
              var temp2 = temp[i].split(/\r?\n/);
              rbt_names = rbt_names.concat(temp2);
          }

          this._vis3.update(rbt_names, "health");
      } else {
          setTimeout(this.setupVis3, 500);
      }
    },
    vis3_update() {
        var temp = this.message.split(" ");
        var rbt_names = [];
        for (var i = 0; i < temp.length; i++) {
            var temp2 = temp[i].split(/\r?\n/);
            rbt_names = rbt_names.concat(temp2);
        }
        //console.log(rbt_names);
        this._vis3.update(rbt_names, "health");
    }
  },
  mounted() {
    this.setupVis3();
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
#vis3textbox {
    min-height: 300px;
}
#vis3box {
    overflow-x:hidden;
    min-height: 600px;
}
.grid {
    opacity: 0.2;
    stroke-dasharray: 5 5; 
}
.tooltip {
            position: absolute;
            font-size: 12px;
            width:  auto;
            height: auto;
            pointer-events: none;
            background-color: white;
            z-index: 1;
        }
</style>
