<template>
  <div>
      <h2 class="head">Current Robot State</h2>
      <div id="vis1box" class="vis_div">
          <svg id="vis1" class="svg_boxes"></svg>
      </div>
      <div id="vis1btn" class="vis_btn">
          <div class="spacer"></div>
          <button id="btn_name_ascending" class="cat" v-on:click="vis1_switch('name-ascending')">Name Ascending</button>
          <button id="btn_val_ascending" class="cat" v-on:click="vis1_switch('value-ascending')">Value Ascending</button>
          <button id="btn_val_descending" class="cat" v-on:click="vis1_switch('value-descending')">Value Descending</button>
      </div>
  </div>
</template>

<script>

import * as d3 from 'd3'

/* constants */
const _margin = ({top: 10, right: 0, bottom: 50, left: 45});

var _vis1;

var Healthplot = function(){
    this.data;
    this.olddata;
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

    this.yRange;
    this.yDomain;
    this.xRange;
    this.xLength;

    this.setupScales = function(yRange, yDomain, xRange, xLength){

        this.yRange = yRange;
        this.yDomain = yDomain;
        this.xRange = xRange;
        this.xLength = xLength;

        //kind of like the min and max value of range in last tut
        this.yScale = d3.scaleLinear()
            .domain(yDomain)
            .range(yRange);

        this.xScale = d3.scaleBand()
            .domain(d3.range(0, xLength))
            .range(xRange)
            .padding(0.1);

        this.xAxisScale = d3.scaleBand()
            .range(xRange) 
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
            .attr("transform", `translate(${_margin.left}, ${this.height - _margin.bottom})`)
            .attr("class", "x axis")
            .call(this.xAxis);

        // x-axis label
        this.svg.append("text")
            .attr("x", 100)
            .attr("y", this.height - _margin.bottom / 2 + 20)
            .style("text-anchor", "middle")
            .text("Robot Name");

        // y-axis label
        this.svg.append("text")
            .attr("x", _margin.left)
            .attr("y", this.height/2 + 10)
            .attr("transform", `rotate(-90, ${_margin.left / 3}, ${this.height/2})`)
            .style("text-anchor", "middle")
            .text("Health (%)");

    }

    this.createBars = function() {
        
        var yScale = d3.scaleLinear()
            .domain(this.yDomain)
            .range(this.yRange);

        var xScale = d3.scaleBand()
            .domain(d3.range(0, this.xLength))
            .range(this.xRange)
            .padding(0.1);
        
        var h = this.height;

        this.bar = this.svg.selectAll("rect")
            .data(this.data)
            .enter()
            .append("rect")
            .attr("class", "bar")
            .style("fill", function(d) {
                if (d.result > 67) return "lightgreen";
                if (d.result > 33) return "orange";
                else return "red";
                })
            .attr("width", xScale.bandwidth())
            .attr("height", function(d) { 
              return (h - _margin.bottom - yScale(d.result)); 
              })
            .attr("x", function(d, i) { return xScale(i); })
            .attr("y", function(d) { return yScale(d.result); })
            .attr("transform", `translate(${_margin.left}, 0)`)
            .append("svg:title") //now when you hover over the bars, it will tell you which robot it represents
            .text(function(d) {
                return d.result; });
        // same as return d["robot"];
        
        this.svg.selectAll("barlabel")
            .data(this.data)
            .enter()
            .append("text")
                .attr("class", "barlabel")
                .attr("x", function(d) { 
                    return 240-yScale(d.result); 
                    })
                .attr("y", function(d, i) {return xScale(i) + _margin.left*6; })
                .attr("transform", `rotate(-90, ${_margin.left}, ${this.height/2})`)
                .text(function(d) {return d.result; })
                .style("fill", "black");
    }

    this.update = function() {
        //remove old data
        this.svg.selectAll("*")
            .remove();

        //add new data
        this.setupScales([this.height - _margin.bottom, _margin.top], [0, 100], [0, this.width - _margin.left], this.data.length);
        this.setupAxis();
        this.createBars();
    }
}


export default {
  name: 'RobotHealth',
  data () {
    return {
      _vis1: this._vis1
    }
  },
  methods: {

    /* --------------------------------------------------------------------------------------------- */
    /* ------------------------------------- HEALTH BAR CHART -------------------------------------- */
    /* --------------------------------------------------------------------------------------------- */

    // code modified from Scott Murray's example
    // https://alignedleft.com/tutorials/d3/scales
    setupVis1(){
        if (this.$store.state.ROBOT_HEALTH.length > 0) {
            this._vis1 = new Healthplot();
            this._vis1.svg = d3.select("#vis1");
            //match size of svg container in html
            //this._vis1.width = this._vis1.svg.node().getBoundingClientRect().width != undefined ?
            //    this._vis1.svg.node().getBoundingClientRect().width : this._vis1.width; //if undefined
            this._vis1.height = this._vis1.svg.node().getBoundingClientRect().height;
            this._vis1.data = this.$store.state.ROBOT_HEALTH;
            this._vis1.width = this.$store.state.ROBOT_HEALTH.length*30;
            document.getElementById('vis1').setAttribute("width", this.$store.state.ROBOT_HEALTH.length*30+"px");

            this._vis1.setupScales([this._vis1.height - _margin.bottom, _margin.top], [0, 100], [0, this._vis1.width - _margin.left], this._vis1.data.length);
            this._vis1.setupAxis();
            this._vis1.createBars();
        } else {
            setTimeout(this.setupVis1, 500);
        }
    },
    vis1_switch(order) {
            //this._vis1.data = this.$store.state.ROBOT_HEALTH;
            if (order === "name-ascending") {
                this._vis1.data.sort((a, b) => d3.ascending(parseInt(a.robot.slice(1),10), parseInt(b.robot.slice(1),10)));
            }
            if (order === "value-ascending") {
                this._vis1.data.sort((a, b) => a.result - b.result);
            }
            if (order === "value-descending") {
                this._vis1.data.sort((a, b) => b.result - a.result);
            }
            this._vis1.xAxisScale.domain(this._vis1.data.map(d => d.name));
            this._vis1.update();
        }
    
  },
  mounted() {
    this.setupVis1();
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
    overflow: scroll;
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
    min-width: 800px;
    min-height: 500px;
    /*box-sizing: border-box;*/
    margin: 10px auto;
    overflow-x:hidden;
}
#vis1box {
    min-height: 800px;
    overflow-y: scroll;
}
.spacer {
    height: 100px;
    float: left;
    width: 100%;
}
</style>
