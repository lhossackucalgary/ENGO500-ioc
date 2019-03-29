<template>
  <div>
        <h3>Historical Data</h3>
        <svg id="vis4" class="svg_boxes"></svg>
    </div>
</template>

<script>
import * as d3 from 'd3'

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


export default {
  name: 'HistData',
  data () {
    return {
      _vis4: []
    }
  },
  mounted() {
    this.setUpVis7();
  },
  methods: {
    /* --------------------------------------------------------------------------------------------- */
    /* -------------------------------------- SET UP VIS 4 ----------------------------------------- */
    /* --------------------------------------------------------------------------------------------- */

    setupVis4(){
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
    },
    mounted() {
        this.setupVis4();
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
</style>
