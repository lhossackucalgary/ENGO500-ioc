<template>
  <div>
        <h2>Historical Data</h2>
        <h3>Highest, Lowest, and Average Robot Health</h3>
        <div id="vis" class="vis_div"></div>
        <svg id="vis4" class="svg_boxes"></svg>
    </div>
</template>

<script>
import * as d3 from 'd3'
import * as vega from 'vega'
import {default as vegaEmbed} from 'vega-embed'
import * as vegaLite from 'vega-lite'

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

var data;


export default {
  name: 'HistData',
  data () {
    return {
      _vis4: [],
      data: this.data
    }
  },
  mounted() {
    //this.setUpVis4();
    this.getHealthData();
    this.setUpHistChart();
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
        },

        setUpHistChart() {
            if (data.length > 0) {
                var spec = {
                            "$schema": "https://vega.github.io/schema/vega/v5.json",
                            "width": 1400,
                            "height": 480,
                            "padding": 5,

                            "data": data,

                            "signals": [
                                {
                                "name": "detailDomain"
                                }
                            ],

                            "marks": [
                                {
                                "type": "group",
                                "name": "detail",
                                "encode": {
                                    "enter": {
                                    "height": {"value": 390},
                                    "width": {"value": 1400}
                                    }
                                },
                                "scales": [
                                    {
                                    "name": "xDetail",
                                    "type": "time",
                                    "range": "width",
                                    "domain": {"data": "health", "field": "date"},
                                    "domainRaw": {"signal": "detailDomain"}
                                    },
                                    {
                                    "name": "yDetail",
                                    "type": "linear",
                                    "range": [390, 0],
                                    "domain": [0, 100],
                                    "nice": true, "zero": true
                                    },
                                    {
                                    "name": "color",
                                    "type": "ordinal",
                                    "domain": ["highest", "average", "lowest"],
                                    "range": ["lightgreen", "steelblue", "red"]
                                    }
                                ],
                                "marks": [
                                    {
                                    "type": "group",
                                    "encode": {
                                        "enter": {
                                        "height": {"field": {"group": "height"}},
                                        "width": {"field": {"group": "width"}},
                                        "clip": {"value": true}
                                        }
                                    },
                                    "marks": [
                                        {
                                        "type": "line",
                                        "from": {"data": "health"},
                                        "encode": {
                                            "update": {
                                            "x": {"scale": "xDetail", "field": "date"},
                                            "y": {"scale": "yDetail", "field": "high"},
                                            "y2": {"scale": "yDetail", "value": 0},
                                            "stroke": {"value": "lightgreen"},
                                            "strokeWidth": {"value": 2}
                                            }
                                        }
                                        },
                                        {
                                        "type": "symbol",
                                        "from": {"data": "health"},
                                        "encode": {
                                            "update": {
                                            "shape": {"value" : "circle"},
                                            "size": {"value" : 40},
                                            "opacity": {"value" : 0.3},
                                            "x": {"scale": "xDetail", "field": "date"},
                                            "y": {"scale": "yDetail", "field": "high"},
                                            "y2": {"scale": "yDetail", "value": 0},
                                            "stroke": {"value": "lightgreen"},
                                            "strokeWidth": {"value": 2},
                                            "tooltip": {"signal": "{'Date': timeFormat(datum.date, '%b %d 20%y'), 'Highest Health (%)': datum.high}"}
                                            }
                                        }
                                        },
                                        {
                                        "type": "line",
                                        "from": {"data": "health"},
                                        "encode": {
                                            "update": {
                                            "x": {"scale": "xDetail", "field": "date"},
                                            "y": {"scale": "yDetail", "field": "average"},
                                            "y2": {"scale": "yDetail", "value": 0},
                                            "stroke": {"value": "steelblue"},
                                            "strokeWidth": {"value": 2},
                                            }
                                        }
                                        },
                                        {
                                        "type": "symbol",
                                        "from": {"data": "health"},
                                        "encode": {
                                            "update": {
                                            "shape": {"value" : "circle"},
                                            "size": {"value" : 40},
                                            "opacity": {"value" : 0.3},
                                            "x": {"scale": "xDetail", "field": "date"},
                                            "y": {"scale": "yDetail", "field": "average"},
                                            "y2": {"scale": "yDetail", "value": 0},
                                            "stroke": {"value": "steelblue"},
                                            "strokeWidth": {"value": 2},
                                            "tooltip": {"signal": "{'Date': timeFormat(datum.date, '%b %d 20%y'), 'Average Health (%)': datum.average}"}
                                            }
                                        }
                                        },
                                        {
                                        "type": "line",
                                        "from": {"data": "health"},
                                        "encode": {
                                            "update": {
                                            "x": {"scale": "xDetail", "field": "date"},
                                            "y": {"scale": "yDetail", "field": "low"},
                                            "y2": {"scale": "yDetail", "value": 0},
                                            "stroke": {"value": "red"},
                                            "strokeWidth": {"value": 2},
                                            }
                                        }
                                        },
                                        {
                                        "type": "symbol",
                                        "from": {"data": "health"},
                                        "encode": {
                                            "update": {
                                            "shape": {"value" : "circle"},
                                            "size": {"value" : 40},
                                            "opacity": {"value" : 0.3},
                                            "x": {"scale": "xDetail", "field": "date"},
                                            "y": {"scale": "yDetail", "field": "low"},
                                            "y2": {"scale": "yDetail", "value": 0},
                                            "stroke": {"value": "red"},
                                            "strokeWidth": {"value": 2},
                                            "tooltip": {"signal": "{'Date': timeFormat(datum.date, '%b %d 20%y'), 'Lowest Health (%)': datum.low}"}
                                            }
                                        }
                                        }
                                    ]
                                    }
                                ],
                                "axes": [
                                    {"orient": "bottom", "scale": "xDetail", "grid":true, "title":"Date"},
                                    {"orient": "left", "scale": "yDetail", "grid":true, "title":"Health (%)"}
                                ],
                                "legends": [
                                    {"orient": "bottom-right", "fill":"color", "offset": 0, "zindex": 1, "title":"Legend:", "fillColor":"white", "padding": 3,"labelFontSize": 18}
                                ]
                                },

                                {
                                "type": "group",
                                "name": "overview",
                                "encode": {
                                    "enter": {
                                    "x": {"value": 0},
                                    "y": {"value": 430},
                                    "height": {"value": 70},
                                    "width": {"value": 720},
                                    "fill": {"value": "transparent"}
                                    }
                                },
                                "signals": [
                                    {
                                    "name": "brush", "value": 0,
                                    "on": [
                                        {
                                        "events": "@overview:mousedown",
                                        "update": "[x(), x()]"
                                        },
                                        {
                                        "events": "[@overview:mousedown, window:mouseup] > window:mousemove!",
                                        "update": "[brush[0], clamp(x(), 0, width)]"
                                        },
                                        {
                                        "events": {"signal": "delta"},
                                        "update": "clampRange([anchor[0] + delta, anchor[1] + delta], 0, width)"
                                        }
                                    ]
                                    },
                                    {
                                    "name": "anchor", "value": null,
                                    "on": [{"events": "@brush:mousedown", "update": "slice(brush)"}]
                                    },
                                    {
                                    "name": "xdown", "value": 0,
                                    "on": [{"events": "@brush:mousedown", "update": "x()"}]
                                    },
                                    {
                                    "name": "delta", "value": 0,
                                    "on": [
                                        {
                                        "events": "[@brush:mousedown, window:mouseup] > window:mousemove!",
                                        "update": "x() - xdown"
                                        }
                                    ]
                                    },
                                    {
                                    "name": "detailDomain",
                                    "push": "outer",
                                    "on": [
                                        {
                                        "events": {"signal": "brush"},
                                        "update": "span(brush) ? invert('xOverview', brush) : null"
                                        }
                                    ]
                                    }
                                ],
                                "scales": [
                                    {
                                    "name": "xOverview",
                                    "type": "time",
                                    "range": "width",
                                    "domain": {"data": "health", "field": "date"}
                                    },
                                    {
                                    "name": "yOverview",
                                    "type": "linear",
                                    "range": [70, 0],
                                    "domain": [0,100],
                                    "nice": true, "zero": true
                                    }
                                ],
                                "axes": [
                                    {"orient": "bottom", "scale": "xOverview", "title": "Overview"}
                                ],
                                "marks": [
                                    {
                                    "type": "area",
                                    "interactive": false,
                                    "from": {"data": "health"},
                                    "encode": {
                                        "update": {
                                        "x": {"scale": "xOverview", "field": "date"},
                                        "y": {"scale": "yOverview", "field": "high"},
                                        "y2": {"scale": "yOverview", "value": 0},
                                        "stroke": {"value": "lightgreen"},
                                        "strokeWidth": {"value": 1}
                                        }
                                    }
                                    },
                                    {
                                    "type": "area",
                                    "interactive": false,
                                    "from": {"data": "health"},
                                    "encode": {
                                        "update": {
                                        "x": {"scale": "xOverview", "field": "date"},
                                        "y": {"scale": "yOverview", "field": "average"},
                                        "y2": {"scale": "yOverview", "value": 0},
                                        "stroke": {"value": "steelblue"},
                                        "strokeWidth": {"value": 1}
                                        }
                                    }
                                    },
                                    {
                                    "type": "area",
                                    "interactive": false,
                                    "from": {"data": "health"},
                                    "encode": {
                                        "update": {
                                        "x": {"scale": "xOverview", "field": "date"},
                                        "y": {"scale": "yOverview", "field": "low"},
                                        "y2": {"scale": "yOverview", "value": 0},
                                        "stroke": {"value": "red"},
                                        "strokeWidth": {"value": 1}
                                        }
                                    }
                                    },
                                    {
                                    "type": "rect",
                                    "name": "brush",
                                    "encode": {
                                        "enter": {
                                        "y": {"value": 0},
                                        "height": {"value": 70},
                                        "fill": {"value": "#333"},
                                        "fillOpacity": {"value": 0.2}
                                        },
                                        "update": {
                                        "x": {"signal": "brush[0]"},
                                        "x2": {"signal": "brush[1]"}
                                        }
                                    }
                                    },
                                    {
                                    "type": "rect",
                                    "interactive": false,
                                    "encode": {
                                        "enter": {
                                        "y": {"value": 0},
                                        "height": {"value": 70},
                                        "width": {"value": 1},
                                        "fill": {"value": "firebrick"}
                                        },
                                        "update": {
                                        "x": {"signal": "brush[0]"}
                                        }
                                    }
                                    },
                                    {
                                    "type": "rect",
                                    "interactive": false,
                                    "encode": {
                                        "enter": {
                                        "y": {"value": 0},
                                        "height": {"value": 70},
                                        "width": {"value": 1},
                                        "fill": {"value": "firebrick"}
                                        },
                                        "update": {
                                        "x": {"signal": "brush[1]"}
                                        }
                                    }
                                    }
                                ]
                                }
                            ]
                            }
                            vegaEmbed('#vis', spec).then(function(result) {

                            // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
                            }).catch(console.error);
            } else {
                setTimeout(this.setUpHistChart, 500);
            }
            
        },
        getHealthData() {

            data = [{
                "name": "health",
                "values": [
                { "date": "01 Jul 2017 00:00:00 GMT-6", "average": 76, "high": 94, "low": 28},
                { "date": "02 Jul 2017 00:00:00 GMT-6", "average": 83, "high": 86, "low": 42},
                { "date": "03 Jul 2017 00:00:00 GMT-6", "average": 85, "high": 94, "low": 20},
                { "date": "04 Jul 2017 00:00:00 GMT-6", "average": 76, "high": 89, "low": 12},
                { "date": "05 Jul 2017 00:00:00 GMT-6", "average": 71, "high": 98, "low": 33},
                { "date": "06 Jul 2017 00:00:00 GMT-6", "average": 78, "high": 86, "low": 5},
                { "date": "07 Jul 2017 00:00:00 GMT-6", "average": 88, "high": 93, "low": 49},
                { "date": "08 Jul 2017 00:00:00 GMT-6", "average": 77, "high": 87, "low": 28},
                { "date": "09 Jul 2017 00:00:00 GMT-6", "average": 89, "high": 99, "low": 51},
                { "date": "10 Jul 2017 00:00:00 GMT-6", "average": 70, "high": 97, "low": 27},
                { "date": "11 Jul 2017 00:00:00 GMT-6", "average": 76, "high": 92, "low": 24},
                { "date": "12 Jul 2017 00:00:00 GMT-6", "average": 80, "high": 92, "low": 41},
                { "date": "13 Jul 2017 00:00:00 GMT-6", "average": 89, "high": 88, "low": 54},
                { "date": "14 Jul 2017 00:00:00 GMT-6", "average": 84, "high": 92, "low": 47},
                { "date": "15 Jul 2017 00:00:00 GMT-6", "average": 77, "high": 99, "low": 9},
                { "date": "16 Jul 2017 00:00:00 GMT-6", "average": 72, "high": 88, "low": 35},
                { "date": "17 Jul 2017 00:00:00 GMT-6", "average": 81, "high": 93, "low": 48},
                { "date": "18 Jul 2017 00:00:00 GMT-6", "average": 75, "high": 93, "low": 51},
                { "date": "19 Jul 2017 00:00:00 GMT-6", "average": 73, "high": 93, "low": 0},
                { "date": "20 Jul 2017 00:00:00 GMT-6", "average": 74, "high": 93, "low": 9},
                { "date": "21 Jul 2017 00:00:00 GMT-6", "average": 76, "high": 95, "low": 22},
                { "date": "22 Jul 2017 00:00:00 GMT-6", "average": 84, "high": 89, "low": 50},
                { "date": "23 Jul 2017 00:00:00 GMT-6", "average": 90, "high": 97, "low": 53},
                { "date": "24 Jul 2017 00:00:00 GMT-6", "average": 85, "high": 99, "low": 50},
                { "date": "25 Jul 2017 00:00:00 GMT-6", "average": 85, "high": 96, "low": 10},
                { "date": "26 Jul 2017 00:00:00 GMT-6", "average": 82, "high": 96, "low": 60},
                { "date": "27 Jul 2017 00:00:00 GMT-6", "average": 87, "high": 87, "low": 24},
                { "date": "28 Jul 2017 00:00:00 GMT-6", "average": 86, "high": 86, "low": 32},
                { "date": "29 Jul 2017 00:00:00 GMT-6", "average": 89, "high": 99, "low": 57},
                { "date": "30 Jul 2017 00:00:00 GMT-6", "average": 85, "high": 91, "low": 37},
                { "date": "31 Jul 2017 00:00:00 GMT-6", "average": 90, "high": 86, "low": 22},
                { "date": "01 Aug 2017 00:00:00 GMT-6", "average": 76, "high": 100, "low": 8},
                { "date": "02 Aug 2017 00:00:00 GMT-6", "average": 72, "high": 98, "low": 29},
                { "date": "03 Aug 2017 00:00:00 GMT-6", "average": 79, "high": 95, "low": 29},
                { "date": "04 Aug 2017 00:00:00 GMT-6", "average": 87, "high": 85, "low": 6},
                { "date": "05 Aug 2017 00:00:00 GMT-6", "average": 77, "high": 89, "low": 14},
                { "date": "06 Aug 2017 00:00:00 GMT-6", "average": 80, "high": 98, "low": 53},
                { "date": "07 Aug 2017 00:00:00 GMT-6", "average": 88, "high": 98, "low": 51},
                { "date": "08 Aug 2017 00:00:00 GMT-6", "average": 82, "high": 95, "low": 30},
                { "date": "09 Aug 2017 00:00:00 GMT-6", "average": 83, "high": 98, "low": 15},
                { "date": "10 Aug 2017 00:00:00 GMT-6", "average": 83, "high": 88, "low": 60},
                { "date": "11 Aug 2017 00:00:00 GMT-6", "average": 80, "high": 87, "low": 46},
                { "date": "12 Aug 2017 00:00:00 GMT-6", "average": 80, "high": 89, "low": 57},
                { "date": "13 Aug 2017 00:00:00 GMT-6", "average": 70, "high": 91, "low": 7},
                { "date": "14 Aug 2017 00:00:00 GMT-6", "average": 78, "high": 90, "low": 15},
                { "date": "15 Aug 2017 00:00:00 GMT-6", "average": 84, "high": 97, "low": 38},
                { "date": "16 Aug 2017 00:00:00 GMT-6", "average": 82, "high": 85, "low": 60},
                { "date": "17 Aug 2017 00:00:00 GMT-6", "average": 84, "high": 96, "low": 47},
                { "date": "18 Aug 2017 00:00:00 GMT-6", "average": 86, "high": 99, "low": 58},
                { "date": "19 Aug 2017 00:00:00 GMT-6", "average": 84, "high": 89, "low": 32},
                { "date": "20 Aug 2017 00:00:00 GMT-6", "average": 90, "high": 91, "low": 49},
                { "date": "21 Aug 2017 00:00:00 GMT-6", "average": 84, "high": 100, "low": 51},
                { "date": "22 Aug 2017 00:00:00 GMT-6", "average": 82, "high": 96, "low": 46},
                { "date": "23 Aug 2017 00:00:00 GMT-6", "average": 74, "high": 92, "low": 11},
                { "date": "24 Aug 2017 00:00:00 GMT-6", "average": 85, "high": 94, "low": 28},
                { "date": "25 Aug 2017 00:00:00 GMT-6", "average": 71, "high": 85, "low": 52},
                { "date": "26 Aug 2017 00:00:00 GMT-6", "average": 82, "high": 93, "low": 3},
                { "date": "27 Aug 2017 00:00:00 GMT-6", "average": 89, "high": 93, "low": 5},
                { "date": "28 Aug 2017 00:00:00 GMT-6", "average": 76, "high": 97, "low": 28},
                { "date": "29 Aug 2017 00:00:00 GMT-6", "average": 73, "high": 99, "low": 37},
                { "date": "30 Aug 2017 00:00:00 GMT-6", "average": 85, "high": 93, "low": 53},
                { "date": "31 Aug 2017 00:00:00 GMT-6", "average": 81, "high": 94, "low": 57},
                { "date": "01 Sep 2017 00:00:00 GMT-6", "average": 75, "high": 95, "low": 44},
                { "date": "02 Sep 2017 00:00:00 GMT-6", "average": 74, "high": 93, "low": 36},
                { "date": "03 Sep 2017 00:00:00 GMT-6", "average": 86, "high": 94, "low": 21},
                { "date": "04 Sep 2017 00:00:00 GMT-6", "average": 90, "high": 87, "low": 24},
                { "date": "05 Sep 2017 00:00:00 GMT-6", "average": 82, "high": 94, "low": 39},
                { "date": "06 Sep 2017 00:00:00 GMT-6", "average": 85, "high": 97, "low": 42},
                { "date": "07 Sep 2017 00:00:00 GMT-6", "average": 79, "high": 100, "low": 47},
                { "date": "08 Sep 2017 00:00:00 GMT-6", "average": 79, "high": 90, "low": 44},
                { "date": "09 Sep 2017 00:00:00 GMT-6", "average": 84, "high": 90, "low": 38},
                { "date": "10 Sep 2017 00:00:00 GMT-6", "average": 80, "high": 91, "low": 56},
                { "date": "11 Sep 2017 00:00:00 GMT-6", "average": 78, "high": 92, "low": 5},
                { "date": "12 Sep 2017 00:00:00 GMT-6", "average": 72, "high": 92, "low": 25},
                { "date": "13 Sep 2017 00:00:00 GMT-6", "average": 80, "high": 86, "low": 32},
                { "date": "14 Sep 2017 00:00:00 GMT-6", "average": 70, "high": 86, "low": 22},
                { "date": "15 Sep 2017 00:00:00 GMT-6", "average": 83, "high": 90, "low": 3},
                { "date": "16 Sep 2017 00:00:00 GMT-6", "average": 86, "high": 86, "low": 10},
                { "date": "17 Sep 2017 00:00:00 GMT-6", "average": 74, "high": 100, "low": 8},
                { "date": "18 Sep 2017 00:00:00 GMT-6", "average": 71, "high": 85, "low": 17},
                { "date": "19 Sep 2017 00:00:00 GMT-6", "average": 70, "high": 96, "low": 1},
                { "date": "20 Sep 2017 00:00:00 GMT-6", "average": 73, "high": 93, "low": 38},
                { "date": "21 Sep 2017 00:00:00 GMT-6", "average": 74, "high": 97, "low": 2},
                { "date": "22 Sep 2017 00:00:00 GMT-6", "average": 89, "high": 89, "low": 52},
                { "date": "23 Sep 2017 00:00:00 GMT-6", "average": 74, "high": 99, "low": 5},
                { "date": "24 Sep 2017 00:00:00 GMT-6", "average": 70, "high": 86, "low": 57},
                { "date": "25 Sep 2017 00:00:00 GMT-6", "average": 73, "high": 93, "low": 4},
                { "date": "26 Sep 2017 00:00:00 GMT-6", "average": 83, "high": 91, "low": 6},
                { "date": "27 Sep 2017 00:00:00 GMT-6", "average": 81, "high": 96, "low": 42},
                { "date": "28 Sep 2017 00:00:00 GMT-6", "average": 89, "high": 92, "low": 46},
                { "date": "29 Sep 2017 00:00:00 GMT-6", "average": 80, "high": 99, "low": 39},
                { "date": "30 Sep 2017 00:00:00 GMT-6", "average": 71, "high": 90, "low": 40},
                { "date": "01 Oct 2017 00:00:00 GMT-6", "average": 87, "high": 96, "low": 17},
                { "date": "02 Oct 2017 00:00:00 GMT-6", "average": 78, "high": 93, "low": 46},
                { "date": "03 Oct 2017 00:00:00 GMT-6", "average": 85, "high": 88, "low": 15},
                { "date": "04 Oct 2017 00:00:00 GMT-6", "average": 80, "high": 88, "low": 3},
                { "date": "05 Oct 2017 00:00:00 GMT-6", "average": 77, "high": 93, "low": 7},
                { "date": "06 Oct 2017 00:00:00 GMT-6", "average": 73, "high": 86, "low": 60},
                { "date": "07 Oct 2017 00:00:00 GMT-6", "average": 70, "high": 91, "low": 29},
                { "date": "08 Oct 2017 00:00:00 GMT-6", "average": 81, "high": 95, "low": 26},
                { "date": "09 Oct 2017 00:00:00 GMT-6", "average": 78, "high": 98, "low": 32},
                { "date": "10 Oct 2017 00:00:00 GMT-6", "average": 85, "high": 87, "low": 47},
                { "date": "11 Oct 2017 00:00:00 GMT-6", "average": 85, "high": 97, "low": 30},
                { "date": "12 Oct 2017 00:00:00 GMT-6", "average": 87, "high": 86, "low": 25},
                { "date": "13 Oct 2017 00:00:00 GMT-6", "average": 87, "high": 90, "low": 58},
                { "date": "14 Oct 2017 00:00:00 GMT-6", "average": 76, "high": 98, "low": 16},
                { "date": "15 Oct 2017 00:00:00 GMT-6", "average": 85, "high": 87, "low": 59},
                { "date": "16 Oct 2017 00:00:00 GMT-6", "average": 86, "high": 94, "low": 59},
                { "date": "17 Oct 2017 00:00:00 GMT-6", "average": 77, "high": 90, "low": 58},
                { "date": "18 Oct 2017 00:00:00 GMT-6", "average": 83, "high": 100, "low": 28},
                { "date": "19 Oct 2017 00:00:00 GMT-6", "average": 85, "high": 85, "low": 35},
                { "date": "20 Oct 2017 00:00:00 GMT-6", "average": 86, "high": 93, "low": 28},
                { "date": "21 Oct 2017 00:00:00 GMT-6", "average": 86, "high": 98, "low": 19},
                { "date": "22 Oct 2017 00:00:00 GMT-6", "average": 77, "high": 88, "low": 2},
                { "date": "23 Oct 2017 00:00:00 GMT-6", "average": 83, "high": 86, "low": 56},
                { "date": "24 Oct 2017 00:00:00 GMT-6", "average": 82, "high": 87, "low": 6},
                { "date": "25 Oct 2017 00:00:00 GMT-6", "average": 74, "high": 94, "low": 5},
                { "date": "26 Oct 2017 00:00:00 GMT-6", "average": 77, "high": 97, "low": 46},
                { "date": "27 Oct 2017 00:00:00 GMT-6", "average": 77, "high": 91, "low": 55},
                { "date": "28 Oct 2017 00:00:00 GMT-6", "average": 90, "high": 87, "low": 44},
                { "date": "29 Oct 2017 00:00:00 GMT-6", "average": 90, "high": 97, "low": 36},
                { "date": "30 Oct 2017 00:00:00 GMT-6", "average": 73, "high": 92, "low": 15},
                { "date": "31 Oct 2017 00:00:00 GMT-6", "average": 80, "high": 97, "low": 19},
                { "date": "01 Nov 2017 00:00:00 GMT-6", "average": 77, "high": 100, "low": 45},
                { "date": "02 Nov 2017 00:00:00 GMT-6", "average": 90, "high": 98, "low": 9},
                { "date": "03 Nov 2017 00:00:00 GMT-6", "average": 83, "high": 98, "low": 39},
                { "date": "04 Nov 2017 00:00:00 GMT-6", "average": 76, "high": 100, "low": 25},
                { "date": "05 Nov 2017 00:00:00 GMT-6", "average": 79, "high": 97, "low": 12},
                { "date": "06 Nov 2017 00:00:00 GMT-6", "average": 80, "high": 87, "low": 39},
                { "date": "07 Nov 2017 00:00:00 GMT-6", "average": 89, "high": 90, "low": 36},
                { "date": "08 Nov 2017 00:00:00 GMT-6", "average": 88, "high": 98, "low": 51},
                { "date": "09 Nov 2017 00:00:00 GMT-6", "average": 83, "high": 85, "low": 58},
                { "date": "10 Nov 2017 00:00:00 GMT-6", "average": 79, "high": 100, "low": 6},
                { "date": "11 Nov 2017 00:00:00 GMT-6", "average": 76, "high": 96, "low": 22},
                { "date": "12 Nov 2017 00:00:00 GMT-6", "average": 90, "high": 98, "low": 32},
                { "date": "13 Nov 2017 00:00:00 GMT-6", "average": 73, "high": 99, "low": 53},
                { "date": "14 Nov 2017 00:00:00 GMT-6", "average": 77, "high": 100, "low": 2},
                { "date": "15 Nov 2017 00:00:00 GMT-6", "average": 84, "high": 99, "low": 11},
                { "date": "16 Nov 2017 00:00:00 GMT-6", "average": 79, "high": 88, "low": 13},
                { "date": "17 Nov 2017 00:00:00 GMT-6", "average": 76, "high": 92, "low": 14},
                { "date": "18 Nov 2017 00:00:00 GMT-6", "average": 78, "high": 92, "low": 14},
                { "date": "19 Nov 2017 00:00:00 GMT-6", "average": 77, "high": 97, "low": 28},
                { "date": "20 Nov 2017 00:00:00 GMT-6", "average": 79, "high": 86, "low": 15},
                { "date": "21 Nov 2017 00:00:00 GMT-6", "average": 76, "high": 94, "low": 34},
                { "date": "22 Nov 2017 00:00:00 GMT-6", "average": 83, "high": 95, "low": 39},
                { "date": "23 Nov 2017 00:00:00 GMT-6", "average": 86, "high": 96, "low": 31},
                { "date": "24 Nov 2017 00:00:00 GMT-6", "average": 70, "high": 99, "low": 56},
                { "date": "25 Nov 2017 00:00:00 GMT-6", "average": 77, "high": 89, "low": 46},
                { "date": "26 Nov 2017 00:00:00 GMT-6", "average": 73, "high": 87, "low": 2},
                { "date": "27 Nov 2017 00:00:00 GMT-6", "average": 75, "high": 97, "low": 43},
                { "date": "28 Nov 2017 00:00:00 GMT-6", "average": 78, "high": 90, "low": 59},
                { "date": "29 Nov 2017 00:00:00 GMT-6", "average": 88, "high": 87, "low": 17},
                { "date": "30 Nov 2017 00:00:00 GMT-6", "average": 72, "high": 100, "low": 34},
                { "date": "01 Dec 2017 00:00:00 GMT-6", "average": 82, "high": 90, "low": 52},
                { "date": "02 Dec 2017 00:00:00 GMT-6", "average": 89, "high": 85, "low": 12},
                { "date": "03 Dec 2017 00:00:00 GMT-6", "average": 89, "high": 85, "low": 56},
                { "date": "04 Dec 2017 00:00:00 GMT-6", "average": 77, "high": 88, "low": 22},
                { "date": "05 Dec 2017 00:00:00 GMT-6", "average": 86, "high": 96, "low": 54},
                { "date": "06 Dec 2017 00:00:00 GMT-6", "average": 77, "high": 87, "low": 21},
                { "date": "07 Dec 2017 00:00:00 GMT-6", "average": 71, "high": 92, "low": 12},
                { "date": "08 Dec 2017 00:00:00 GMT-6", "average": 90, "high": 87, "low": 43},
                { "date": "09 Dec 2017 00:00:00 GMT-6", "average": 75, "high": 93, "low": 26},
                { "date": "10 Dec 2017 00:00:00 GMT-6", "average": 76, "high": 94, "low": 25},
                { "date": "11 Dec 2017 00:00:00 GMT-6", "average": 80, "high": 87, "low": 3},
                { "date": "12 Dec 2017 00:00:00 GMT-6", "average": 88, "high": 90, "low": 44},
                { "date": "13 Dec 2017 00:00:00 GMT-6", "average": 78, "high": 91, "low": 5},
                { "date": "14 Dec 2017 00:00:00 GMT-6", "average": 71, "high": 90, "low": 52},
                { "date": "15 Dec 2017 00:00:00 GMT-6", "average": 70, "high": 98, "low": 22},
                { "date": "16 Dec 2017 00:00:00 GMT-6", "average": 82, "high": 95, "low": 50},
                { "date": "17 Dec 2017 00:00:00 GMT-6", "average": 79, "high": 85, "low": 45},
                { "date": "18 Dec 2017 00:00:00 GMT-6", "average": 83, "high": 98, "low": 28},
                { "date": "19 Dec 2017 00:00:00 GMT-6", "average": 70, "high": 97, "low": 55},
                { "date": "20 Dec 2017 00:00:00 GMT-6", "average": 87, "high": 85, "low": 7},
                { "date": "21 Dec 2017 00:00:00 GMT-6", "average": 74, "high": 91, "low": 1},
                { "date": "22 Dec 2017 00:00:00 GMT-6", "average": 90, "high": 87, "low": 57},
                { "date": "23 Dec 2017 00:00:00 GMT-6", "average": 75, "high": 90, "low": 50},
                { "date": "24 Dec 2017 00:00:00 GMT-6", "average": 77, "high": 97, "low": 5},
                { "date": "25 Dec 2017 00:00:00 GMT-6", "average": 84, "high": 87, "low": 42},
                { "date": "26 Dec 2017 00:00:00 GMT-6", "average": 77, "high": 97, "low": 26},
                { "date": "27 Dec 2017 00:00:00 GMT-6", "average": 88, "high": 95, "low": 1},
                { "date": "28 Dec 2017 00:00:00 GMT-6", "average": 89, "high": 85, "low": 25},
                { "date": "29 Dec 2017 00:00:00 GMT-6", "average": 79, "high": 99, "low": 30},
                { "date": "30 Dec 2017 00:00:00 GMT-6", "average": 85, "high": 94, "low": 37},
                { "date": "31 Dec 2017 00:00:00 GMT-6", "average": 76, "high": 86, "low": 60},
                { "date": "01 Jan 2018 00:00:00 GMT-6", "average": 80, "high": 98, "low": 14},
                { "date": "02 Jan 2018 00:00:00 GMT-6", "average": 79, "high": 89, "low": 56},
                { "date": "03 Jan 2018 00:00:00 GMT-6", "average": 87, "high": 99, "low": 11},
                { "date": "04 Jan 2018 00:00:00 GMT-6", "average": 70, "high": 89, "low": 16},
                { "date": "05 Jan 2018 00:00:00 GMT-6", "average": 72, "high": 100, "low": 45},
                { "date": "06 Jan 2018 00:00:00 GMT-6", "average": 77, "high": 90, "low": 8},
                { "date": "07 Jan 2018 00:00:00 GMT-6", "average": 79, "high": 90, "low": 57},
                { "date": "08 Jan 2018 00:00:00 GMT-6", "average": 79, "high": 91, "low": 1},
                { "date": "09 Jan 2018 00:00:00 GMT-6", "average": 84, "high": 88, "low": 14},
                { "date": "10 Jan 2018 00:00:00 GMT-6", "average": 85, "high": 87, "low": 29},
                { "date": "11 Jan 2018 00:00:00 GMT-6", "average": 78, "high": 92, "low": 60},
                { "date": "12 Jan 2018 00:00:00 GMT-6", "average": 76, "high": 98, "low": 57},
                { "date": "13 Jan 2018 00:00:00 GMT-6", "average": 83, "high": 85, "low": 49},
                { "date": "14 Jan 2018 00:00:00 GMT-6", "average": 74, "high": 91, "low": 9},
                { "date": "15 Jan 2018 00:00:00 GMT-6", "average": 89, "high": 100, "low": 39},
                { "date": "16 Jan 2018 00:00:00 GMT-6", "average": 70, "high": 87, "low": 0},
                { "date": "17 Jan 2018 00:00:00 GMT-6", "average": 80, "high": 99, "low": 50},
                { "date": "18 Jan 2018 00:00:00 GMT-6", "average": 77, "high": 85, "low": 53},
                { "date": "19 Jan 2018 00:00:00 GMT-6", "average": 73, "high": 100, "low": 17},
                { "date": "20 Jan 2018 00:00:00 GMT-6", "average": 76, "high": 89, "low": 57},
                { "date": "21 Jan 2018 00:00:00 GMT-6", "average": 74, "high": 92, "low": 7},
                { "date": "22 Jan 2018 00:00:00 GMT-6", "average": 83, "high": 87, "low": 14},
                { "date": "23 Jan 2018 00:00:00 GMT-6", "average": 80, "high": 88, "low": 45},
                { "date": "24 Jan 2018 00:00:00 GMT-6", "average": 71, "high": 99, "low": 57},
                { "date": "25 Jan 2018 00:00:00 GMT-6", "average": 77, "high": 95, "low": 5},
                { "date": "26 Jan 2018 00:00:00 GMT-6", "average": 86, "high": 87, "low": 41},
                { "date": "27 Jan 2018 00:00:00 GMT-6", "average": 80, "high": 91, "low": 51},
                { "date": "28 Jan 2018 00:00:00 GMT-6", "average": 78, "high": 86, "low": 6},
                { "date": "29 Jan 2018 00:00:00 GMT-6", "average": 82, "high": 90, "low": 47},
                { "date": "30 Jan 2018 00:00:00 GMT-6", "average": 75, "high": 92, "low": 20},
                { "date": "31 Jan 2018 00:00:00 GMT-6", "average": 73, "high": 93, "low": 32},
                { "date": "01 Feb 2018 00:00:00 GMT-6", "average": 71, "high": 89, "low": 16},
                { "date": "02 Feb 2018 00:00:00 GMT-6", "average": 76, "high": 86, "low": 42},
                { "date": "03 Feb 2018 00:00:00 GMT-6", "average": 75, "high": 90, "low": 7},
                { "date": "04 Feb 2018 00:00:00 GMT-6", "average": 75, "high": 91, "low": 53},
                { "date": "05 Feb 2018 00:00:00 GMT-6", "average": 77, "high": 98, "low": 54},
                { "date": "06 Feb 2018 00:00:00 GMT-6", "average": 77, "high": 95, "low": 4},
                { "date": "07 Feb 2018 00:00:00 GMT-6", "average": 83, "high": 95, "low": 56},
                { "date": "08 Feb 2018 00:00:00 GMT-6", "average": 76, "high": 99, "low": 60},
                { "date": "09 Feb 2018 00:00:00 GMT-6", "average": 83, "high": 93, "low": 15},
                { "date": "10 Feb 2018 00:00:00 GMT-6", "average": 85, "high": 87, "low": 39},
                { "date": "11 Feb 2018 00:00:00 GMT-6", "average": 85, "high": 100, "low": 22},
                { "date": "12 Feb 2018 00:00:00 GMT-6", "average": 87, "high": 88, "low": 5},
                { "date": "13 Feb 2018 00:00:00 GMT-6", "average": 77, "high": 85, "low": 36},
                { "date": "14 Feb 2018 00:00:00 GMT-6", "average": 83, "high": 85, "low": 40},
                { "date": "15 Feb 2018 00:00:00 GMT-6", "average": 89, "high": 85, "low": 42},
                { "date": "16 Feb 2018 00:00:00 GMT-6", "average": 79, "high": 87, "low": 11},
                { "date": "17 Feb 2018 00:00:00 GMT-6", "average": 89, "high": 98, "low": 5},
                { "date": "18 Feb 2018 00:00:00 GMT-6", "average": 73, "high": 96, "low": 16},
                { "date": "19 Feb 2018 00:00:00 GMT-6", "average": 90, "high": 92, "low": 33},
                { "date": "20 Feb 2018 00:00:00 GMT-6", "average": 75, "high": 89, "low": 34},
                { "date": "21 Feb 2018 00:00:00 GMT-6", "average": 73, "high": 97, "low": 51},
                { "date": "22 Feb 2018 00:00:00 GMT-6", "average": 86, "high": 87, "low": 3},
                { "date": "23 Feb 2018 00:00:00 GMT-6", "average": 90, "high": 94, "low": 23},
                { "date": "24 Feb 2018 00:00:00 GMT-6", "average": 70, "high": 98, "low": 7},
                { "date": "25 Feb 2018 00:00:00 GMT-6", "average": 81, "high": 92, "low": 7},
                { "date": "26 Feb 2018 00:00:00 GMT-6", "average": 80, "high": 96, "low": 32},
                { "date": "27 Feb 2018 00:00:00 GMT-6", "average": 75, "high": 91, "low": 1},
                { "date": "28 Feb 2018 00:00:00 GMT-6", "average": 83, "high": 86, "low": 22},
                { "date": "01 Mar 2018 00:00:00 GMT-6", "average": 81, "high": 97, "low": 41},
                { "date": "02 Mar 2018 00:00:00 GMT-6", "average": 79, "high": 98, "low": 32},
                { "date": "03 Mar 2018 00:00:00 GMT-6", "average": 78, "high": 87, "low": 21},
                { "date": "04 Mar 2018 00:00:00 GMT-6", "average": 76, "high": 89, "low": 40},
                { "date": "05 Mar 2018 00:00:00 GMT-6", "average": 73, "high": 94, "low": 19},
                { "date": "06 Mar 2018 00:00:00 GMT-6", "average": 76, "high": 98, "low": 50},
                { "date": "07 Mar 2018 00:00:00 GMT-6", "average": 70, "high": 88, "low": 38},
                { "date": "08 Mar 2018 00:00:00 GMT-6", "average": 76, "high": 96, "low": 17},
                { "date": "09 Mar 2018 00:00:00 GMT-6", "average": 87, "high": 89, "low": 13},
                { "date": "10 Mar 2018 00:00:00 GMT-6", "average": 75, "high": 99, "low": 10},
                { "date": "11 Mar 2018 00:00:00 GMT-6", "average": 89, "high": 85, "low": 10},
                { "date": "12 Mar 2018 00:00:00 GMT-6", "average": 80, "high": 89, "low": 15},
                { "date": "13 Mar 2018 00:00:00 GMT-6", "average": 80, "high": 87, "low": 36},
                { "date": "14 Mar 2018 00:00:00 GMT-6", "average": 82, "high": 86, "low": 53},
                { "date": "15 Mar 2018 00:00:00 GMT-6", "average": 79, "high": 100, "low": 12},
                { "date": "16 Mar 2018 00:00:00 GMT-6", "average": 81, "high": 89, "low": 17},
                { "date": "17 Mar 2018 00:00:00 GMT-6", "average": 74, "high": 93, "low": 58},
                { "date": "18 Mar 2018 00:00:00 GMT-6", "average": 89, "high": 97, "low": 41},
                { "date": "19 Mar 2018 00:00:00 GMT-6", "average": 75, "high": 88, "low": 29},
                { "date": "20 Mar 2018 00:00:00 GMT-6", "average": 84, "high": 99, "low": 48},
                { "date": "21 Mar 2018 00:00:00 GMT-6", "average": 70, "high": 88, "low": 31},
                { "date": "22 Mar 2018 00:00:00 GMT-6", "average": 87, "high": 97, "low": 19},
                { "date": "23 Mar 2018 00:00:00 GMT-6", "average": 88, "high": 99, "low": 28},
                { "date": "24 Mar 2018 00:00:00 GMT-6", "average": 81, "high": 93, "low": 36},
                { "date": "25 Mar 2018 00:00:00 GMT-6", "average": 73, "high": 95, "low": 54},
                { "date": "26 Mar 2018 00:00:00 GMT-6", "average": 90, "high": 92, "low": 6},
                { "date": "27 Mar 2018 00:00:00 GMT-6", "average": 73, "high": 100, "low": 19},
                { "date": "28 Mar 2018 00:00:00 GMT-6", "average": 83, "high": 85, "low": 31},
                { "date": "29 Mar 2018 00:00:00 GMT-6", "average": 78, "high": 97, "low": 27},
                { "date": "30 Mar 2018 00:00:00 GMT-6", "average": 75, "high": 90, "low": 50},
                { "date": "31 Mar 2018 00:00:00 GMT-6", "average": 87, "high": 94, "low": 28},
                { "date": "01 Apr 2018 00:00:00 GMT-6", "average": 83, "high": 86, "low": 53},
                { "date": "02 Apr 2018 00:00:00 GMT-6", "average": 79, "high": 96, "low": 41},
                { "date": "03 Apr 2018 00:00:00 GMT-6", "average": 75, "high": 99, "low": 52},
                { "date": "04 Apr 2018 00:00:00 GMT-6", "average": 86, "high": 96, "low": 45},
                { "date": "05 Apr 2018 00:00:00 GMT-6", "average": 74, "high": 100, "low": 21},
                { "date": "06 Apr 2018 00:00:00 GMT-6", "average": 89, "high": 90, "low": 44},
                { "date": "07 Apr 2018 00:00:00 GMT-6", "average": 89, "high": 98, "low": 39},
                { "date": "08 Apr 2018 00:00:00 GMT-6", "average": 86, "high": 94, "low": 1},
                { "date": "09 Apr 2018 00:00:00 GMT-6", "average": 88, "high": 92, "low": 15},
                { "date": "10 Apr 2018 00:00:00 GMT-6", "average": 72, "high": 88, "low": 43},
                { "date": "11 Apr 2018 00:00:00 GMT-6", "average": 85, "high": 88, "low": 14},
                { "date": "12 Apr 2018 00:00:00 GMT-6", "average": 85, "high": 100, "low": 3},
                { "date": "13 Apr 2018 00:00:00 GMT-6", "average": 76, "high": 96, "low": 60},
                { "date": "14 Apr 2018 00:00:00 GMT-6", "average": 70, "high": 97, "low": 33},
                { "date": "15 Apr 2018 00:00:00 GMT-6", "average": 70, "high": 91, "low": 31},
                { "date": "16 Apr 2018 00:00:00 GMT-6", "average": 71, "high": 95, "low": 51},
                { "date": "17 Apr 2018 00:00:00 GMT-6", "average": 90, "high": 89, "low": 54},
                { "date": "18 Apr 2018 00:00:00 GMT-6", "average": 84, "high": 93, "low": 58},
                { "date": "19 Apr 2018 00:00:00 GMT-6", "average": 72, "high": 93, "low": 50},
                { "date": "20 Apr 2018 00:00:00 GMT-6", "average": 81, "high": 89, "low": 22},
                { "date": "21 Apr 2018 00:00:00 GMT-6", "average": 79, "high": 94, "low": 29},
                { "date": "22 Apr 2018 00:00:00 GMT-6", "average": 79, "high": 89, "low": 28},
                { "date": "23 Apr 2018 00:00:00 GMT-6", "average": 70, "high": 97, "low": 13},
                { "date": "24 Apr 2018 00:00:00 GMT-6", "average": 88, "high": 92, "low": 17},
                { "date": "25 Apr 2018 00:00:00 GMT-6", "average": 81, "high": 92, "low": 50},
                { "date": "26 Apr 2018 00:00:00 GMT-6", "average": 79, "high": 92, "low": 41},
                { "date": "27 Apr 2018 00:00:00 GMT-6", "average": 78, "high": 94, "low": 10},
                { "date": "28 Apr 2018 00:00:00 GMT-6", "average": 90, "high": 97, "low": 41},
                { "date": "29 Apr 2018 00:00:00 GMT-6", "average": 89, "high": 91, "low": 3},
                { "date": "30 Apr 2018 00:00:00 GMT-6", "average": 79, "high": 94, "low": 5},
                { "date": "01 May 2018 00:00:00 GMT-6", "average": 88, "high": 94, "low": 23},
                { "date": "02 May 2018 00:00:00 GMT-6", "average": 71, "high": 100, "low": 22},
                { "date": "03 May 2018 00:00:00 GMT-6", "average": 85, "high": 94, "low": 42},
                { "date": "04 May 2018 00:00:00 GMT-6", "average": 83, "high": 89, "low": 32},
                { "date": "05 May 2018 00:00:00 GMT-6", "average": 83, "high": 98, "low": 42},
                { "date": "06 May 2018 00:00:00 GMT-6", "average": 86, "high": 94, "low": 5},
                { "date": "07 May 2018 00:00:00 GMT-6", "average": 75, "high": 92, "low": 17},
                { "date": "08 May 2018 00:00:00 GMT-6", "average": 85, "high": 98, "low": 8},
                { "date": "09 May 2018 00:00:00 GMT-6", "average": 76, "high": 85, "low": 19},
                { "date": "10 May 2018 00:00:00 GMT-6", "average": 80, "high": 95, "low": 57},
                { "date": "11 May 2018 00:00:00 GMT-6", "average": 84, "high": 89, "low": 22},
                { "date": "12 May 2018 00:00:00 GMT-6", "average": 82, "high": 93, "low": 51},
                { "date": "13 May 2018 00:00:00 GMT-6", "average": 77, "high": 92, "low": 1},
                { "date": "14 May 2018 00:00:00 GMT-6", "average": 87, "high": 100, "low": 5},
                { "date": "15 May 2018 00:00:00 GMT-6", "average": 75, "high": 89, "low": 39},
                { "date": "16 May 2018 00:00:00 GMT-6", "average": 70, "high": 86, "low": 55},
                { "date": "17 May 2018 00:00:00 GMT-6", "average": 89, "high": 89, "low": 57},
                { "date": "18 May 2018 00:00:00 GMT-6", "average": 75, "high": 94, "low": 58},
                { "date": "19 May 2018 00:00:00 GMT-6", "average": 83, "high": 92, "low": 54},
                { "date": "20 May 2018 00:00:00 GMT-6", "average": 72, "high": 97, "low": 23},
                { "date": "21 May 2018 00:00:00 GMT-6", "average": 86, "high": 88, "low": 14},
                { "date": "22 May 2018 00:00:00 GMT-6", "average": 80, "high": 90, "low": 18},
                { "date": "23 May 2018 00:00:00 GMT-6", "average": 80, "high": 91, "low": 10},
                { "date": "24 May 2018 00:00:00 GMT-6", "average": 88, "high": 95, "low": 48},
                { "date": "25 May 2018 00:00:00 GMT-6", "average": 75, "high": 85, "low": 28},
                { "date": "26 May 2018 00:00:00 GMT-6", "average": 88, "high": 85, "low": 57},
                { "date": "27 May 2018 00:00:00 GMT-6", "average": 77, "high": 91, "low": 13},
                { "date": "28 May 2018 00:00:00 GMT-6", "average": 82, "high": 87, "low": 60},
                { "date": "29 May 2018 00:00:00 GMT-6", "average": 88, "high": 91, "low": 31},
                { "date": "30 May 2018 00:00:00 GMT-6", "average": 70, "high": 96, "low": 34},
                { "date": "31 May 2018 00:00:00 GMT-6", "average": 72, "high": 94, "low": 0},
                { "date": "01 Jun 2018 00:00:00 GMT-6", "average": 72, "high": 91, "low": 3},
                { "date": "02 Jun 2018 00:00:00 GMT-6", "average": 73, "high": 87, "low": 44},
                { "date": "03 Jun 2018 00:00:00 GMT-6", "average": 90, "high": 100, "low": 45},
                { "date": "04 Jun 2018 00:00:00 GMT-6", "average": 74, "high": 88, "low": 35},
                { "date": "05 Jun 2018 00:00:00 GMT-6", "average": 75, "high": 91, "low": 0},
                { "date": "06 Jun 2018 00:00:00 GMT-6", "average": 80, "high": 98, "low": 4},
                { "date": "07 Jun 2018 00:00:00 GMT-6", "average": 78, "high": 86, "low": 7},
                { "date": "08 Jun 2018 00:00:00 GMT-6", "average": 85, "high": 87, "low": 14},
                { "date": "09 Jun 2018 00:00:00 GMT-6", "average": 70, "high": 97, "low": 11},
                { "date": "10 Jun 2018 00:00:00 GMT-6", "average": 83, "high": 86, "low": 30},
                { "date": "11 Jun 2018 00:00:00 GMT-6", "average": 71, "high": 96, "low": 50},
                { "date": "12 Jun 2018 00:00:00 GMT-6", "average": 74, "high": 87, "low": 35},
                { "date": "13 Jun 2018 00:00:00 GMT-6", "average": 75, "high": 96, "low": 55},
                { "date": "14 Jun 2018 00:00:00 GMT-6", "average": 79, "high": 97, "low": 17},
                { "date": "15 Jun 2018 00:00:00 GMT-6", "average": 73, "high": 90, "low": 47},
                { "date": "16 Jun 2018 00:00:00 GMT-6", "average": 71, "high": 86, "low": 46},
                { "date": "17 Jun 2018 00:00:00 GMT-6", "average": 82, "high": 91, "low": 9},
                { "date": "18 Jun 2018 00:00:00 GMT-6", "average": 79, "high": 96, "low": 6},
                { "date": "19 Jun 2018 00:00:00 GMT-6", "average": 81, "high": 99, "low": 36},
                { "date": "20 Jun 2018 00:00:00 GMT-6", "average": 79, "high": 91, "low": 39},
                { "date": "21 Jun 2018 00:00:00 GMT-6", "average": 90, "high": 99, "low": 6},
                { "date": "22 Jun 2018 00:00:00 GMT-6", "average": 71, "high": 100, "low": 9},
                { "date": "23 Jun 2018 00:00:00 GMT-6", "average": 84, "high": 86, "low": 27},
                { "date": "24 Jun 2018 00:00:00 GMT-6", "average": 78, "high": 92, "low": 0},
                { "date": "25 Jun 2018 00:00:00 GMT-6", "average": 76, "high": 89, "low": 45},
                { "date": "26 Jun 2018 00:00:00 GMT-6", "average": 75, "high": 94, "low": 8},
                { "date": "27 Jun 2018 00:00:00 GMT-6", "average": 76, "high": 88, "low": 24},
                { "date": "28 Jun 2018 00:00:00 GMT-6", "average": 87, "high": 88, "low": 49},
                { "date": "29 Jun 2018 00:00:00 GMT-6", "average": 83, "high": 95, "low": 1},
                { "date": "30 Jun 2018 00:00:00 GMT-6", "average": 76, "high": 100, "low": 55},
                { "date": "01 Jul 2018 00:00:00 GMT-6", "average": 82, "high": 87, "low": 29},
                { "date": "02 Jul 2018 00:00:00 GMT-6", "average": 87, "high": 91, "low": 36},
                { "date": "03 Jul 2018 00:00:00 GMT-6", "average": 84, "high": 88, "low": 59},
                { "date": "04 Jul 2018 00:00:00 GMT-6", "average": 80, "high": 97, "low": 46},
                { "date": "05 Jul 2018 00:00:00 GMT-6", "average": 72, "high": 87, "low": 57},
                { "date": "06 Jul 2018 00:00:00 GMT-6", "average": 83, "high": 95, "low": 38},
                { "date": "07 Jul 2018 00:00:00 GMT-6", "average": 76, "high": 93, "low": 56},
                { "date": "08 Jul 2018 00:00:00 GMT-6", "average": 90, "high": 87, "low": 56},
                { "date": "09 Jul 2018 00:00:00 GMT-6", "average": 81, "high": 89, "low": 59},
                { "date": "10 Jul 2018 00:00:00 GMT-6", "average": 80, "high": 86, "low": 35},
                { "date": "11 Jul 2018 00:00:00 GMT-6", "average": 78, "high": 97, "low": 44},
                { "date": "12 Jul 2018 00:00:00 GMT-6", "average": 83, "high": 97, "low": 46},
                { "date": "13 Jul 2018 00:00:00 GMT-6", "average": 87, "high": 94, "low": 8},
                { "date": "14 Jul 2018 00:00:00 GMT-6", "average": 80, "high": 98, "low": 8},
                { "date": "15 Jul 2018 00:00:00 GMT-6", "average": 70, "high": 95, "low": 26},
                { "date": "16 Jul 2018 00:00:00 GMT-6", "average": 76, "high": 89, "low": 42},
                { "date": "17 Jul 2018 00:00:00 GMT-6", "average": 72, "high": 95, "low": 12},
                { "date": "18 Jul 2018 00:00:00 GMT-6", "average": 76, "high": 98, "low": 57},
                { "date": "19 Jul 2018 00:00:00 GMT-6", "average": 81, "high": 93, "low": 26},
                { "date": "20 Jul 2018 00:00:00 GMT-6", "average": 83, "high": 95, "low": 22},
                { "date": "21 Jul 2018 00:00:00 GMT-6", "average": 71, "high": 96, "low": 58},
                { "date": "22 Jul 2018 00:00:00 GMT-6", "average": 80, "high": 94, "low": 5},
                { "date": "23 Jul 2018 00:00:00 GMT-6", "average": 82, "high": 92, "low": 29},
                { "date": "24 Jul 2018 00:00:00 GMT-6", "average": 76, "high": 99, "low": 58},
                { "date": "25 Jul 2018 00:00:00 GMT-6", "average": 75, "high": 87, "low": 3},
                { "date": "26 Jul 2018 00:00:00 GMT-6", "average": 75, "high": 96, "low": 32},
                { "date": "27 Jul 2018 00:00:00 GMT-6", "average": 78, "high": 89, "low": 29},
                { "date": "28 Jul 2018 00:00:00 GMT-6", "average": 90, "high": 87, "low": 38},
                { "date": "29 Jul 2018 00:00:00 GMT-6", "average": 76, "high": 97, "low": 36},
                { "date": "30 Jul 2018 00:00:00 GMT-6", "average": 75, "high": 97, "low": 18},
                { "date": "31 Jul 2018 00:00:00 GMT-6", "average": 82, "high": 100, "low": 9},
                { "date": "01 Aug 2018 00:00:00 GMT-6", "average": 84, "high": 91, "low": 5},
                { "date": "02 Aug 2018 00:00:00 GMT-6", "average": 87, "high": 99, "low": 50},
                { "date": "03 Aug 2018 00:00:00 GMT-6", "average": 83, "high": 89, "low": 13},
                { "date": "04 Aug 2018 00:00:00 GMT-6", "average": 90, "high": 99, "low": 17},
                { "date": "05 Aug 2018 00:00:00 GMT-6", "average": 80, "high": 89, "low": 19},
                { "date": "06 Aug 2018 00:00:00 GMT-6", "average": 88, "high": 91, "low": 60},
                { "date": "07 Aug 2018 00:00:00 GMT-6", "average": 79, "high": 98, "low": 46},
                { "date": "08 Aug 2018 00:00:00 GMT-6", "average": 87, "high": 97, "low": 51},
                { "date": "09 Aug 2018 00:00:00 GMT-6", "average": 79, "high": 97, "low": 14},
                { "date": "10 Aug 2018 00:00:00 GMT-6", "average": 78, "high": 94, "low": 38},
                { "date": "11 Aug 2018 00:00:00 GMT-6", "average": 90, "high": 88, "low": 52},
                { "date": "12 Aug 2018 00:00:00 GMT-6", "average": 77, "high": 93, "low": 33},
                { "date": "13 Aug 2018 00:00:00 GMT-6", "average": 81, "high": 94, "low": 1},
                { "date": "14 Aug 2018 00:00:00 GMT-6", "average": 71, "high": 98, "low": 38},
                { "date": "15 Aug 2018 00:00:00 GMT-6", "average": 83, "high": 96, "low": 54},
                { "date": "16 Aug 2018 00:00:00 GMT-6", "average": 74, "high": 94, "low": 26},
                { "date": "17 Aug 2018 00:00:00 GMT-6", "average": 73, "high": 94, "low": 2},
                { "date": "18 Aug 2018 00:00:00 GMT-6", "average": 81, "high": 91, "low": 46},
                { "date": "19 Aug 2018 00:00:00 GMT-6", "average": 78, "high": 94, "low": 1},
                { "date": "20 Aug 2018 00:00:00 GMT-6", "average": 76, "high": 97, "low": 42},
                { "date": "21 Aug 2018 00:00:00 GMT-6", "average": 71, "high": 95, "low": 5},
                { "date": "22 Aug 2018 00:00:00 GMT-6", "average": 80, "high": 96, "low": 15},
                { "date": "23 Aug 2018 00:00:00 GMT-6", "average": 76, "high": 97, "low": 20},
                { "date": "24 Aug 2018 00:00:00 GMT-6", "average": 82, "high": 98, "low": 56},
                { "date": "25 Aug 2018 00:00:00 GMT-6", "average": 89, "high": 88, "low": 41},
                { "date": "26 Aug 2018 00:00:00 GMT-6", "average": 90, "high": 94, "low": 52},
                { "date": "27 Aug 2018 00:00:00 GMT-6", "average": 77, "high": 97, "low": 35},
                { "date": "28 Aug 2018 00:00:00 GMT-6", "average": 90, "high": 88, "low": 4},
                { "date": "29 Aug 2018 00:00:00 GMT-6", "average": 79, "high": 93, "low": 5},
                { "date": "30 Aug 2018 00:00:00 GMT-6", "average": 87, "high": 89, "low": 13},
                { "date": "31 Aug 2018 00:00:00 GMT-6", "average": 73, "high": 96, "low": 35},
                { "date": "01 Sep 2018 00:00:00 GMT-6", "average": 82, "high": 91, "low": 51},
                { "date": "02 Sep 2018 00:00:00 GMT-6", "average": 75, "high": 98, "low": 14},
                { "date": "03 Sep 2018 00:00:00 GMT-6", "average": 85, "high": 90, "low": 16},
                { "date": "04 Sep 2018 00:00:00 GMT-6", "average": 71, "high": 96, "low": 5},
                { "date": "05 Sep 2018 00:00:00 GMT-6", "average": 76, "high": 87, "low": 58},
                { "date": "06 Sep 2018 00:00:00 GMT-6", "average": 80, "high": 87, "low": 44},
                { "date": "07 Sep 2018 00:00:00 GMT-6", "average": 89, "high": 92, "low": 17},
                { "date": "08 Sep 2018 00:00:00 GMT-6", "average": 77, "high": 96, "low": 25},
                { "date": "09 Sep 2018 00:00:00 GMT-6", "average": 71, "high": 95, "low": 34},
                { "date": "10 Sep 2018 00:00:00 GMT-6", "average": 80, "high": 85, "low": 13},
                { "date": "11 Sep 2018 00:00:00 GMT-6", "average": 77, "high": 100, "low": 37},
                { "date": "12 Sep 2018 00:00:00 GMT-6", "average": 90, "high": 90, "low": 4},
                { "date": "13 Sep 2018 00:00:00 GMT-6", "average": 78, "high": 89, "low": 43},
                { "date": "14 Sep 2018 00:00:00 GMT-6", "average": 72, "high": 92, "low": 52},
                { "date": "15 Sep 2018 00:00:00 GMT-6", "average": 82, "high": 94, "low": 44},
                { "date": "16 Sep 2018 00:00:00 GMT-6", "average": 71, "high": 94, "low": 0},
                { "date": "17 Sep 2018 00:00:00 GMT-6", "average": 83, "high": 96, "low": 57},
                { "date": "18 Sep 2018 00:00:00 GMT-6", "average": 83, "high": 96, "low": 58},
                { "date": "19 Sep 2018 00:00:00 GMT-6", "average": 79, "high": 97, "low": 49},
                { "date": "20 Sep 2018 00:00:00 GMT-6", "average": 82, "high": 99, "low": 7},
                { "date": "21 Sep 2018 00:00:00 GMT-6", "average": 82, "high": 87, "low": 33},
                { "date": "22 Sep 2018 00:00:00 GMT-6", "average": 71, "high": 90, "low": 50},
                { "date": "23 Sep 2018 00:00:00 GMT-6", "average": 77, "high": 85, "low": 52},
                { "date": "24 Sep 2018 00:00:00 GMT-6", "average": 79, "high": 88, "low": 60},
                { "date": "25 Sep 2018 00:00:00 GMT-6", "average": 75, "high": 85, "low": 58},
                { "date": "26 Sep 2018 00:00:00 GMT-6", "average": 79, "high": 100, "low": 35},
                { "date": "27 Sep 2018 00:00:00 GMT-6", "average": 85, "high": 97, "low": 15},
                { "date": "28 Sep 2018 00:00:00 GMT-6", "average": 86, "high": 95, "low": 50},
                { "date": "29 Sep 2018 00:00:00 GMT-6", "average": 72, "high": 98, "low": 25},
                { "date": "30 Sep 2018 00:00:00 GMT-6", "average": 75, "high": 89, "low": 60},
                { "date": "01 Oct 2018 00:00:00 GMT-6", "average": 75, "high": 98, "low": 53},
                { "date": "02 Oct 2018 00:00:00 GMT-6", "average": 82, "high": 87, "low": 9},
                { "date": "03 Oct 2018 00:00:00 GMT-6", "average": 90, "high": 96, "low": 59},
                { "date": "04 Oct 2018 00:00:00 GMT-6", "average": 87, "high": 90, "low": 15},
                { "date": "05 Oct 2018 00:00:00 GMT-6", "average": 80, "high": 92, "low": 9},
                { "date": "06 Oct 2018 00:00:00 GMT-6", "average": 89, "high": 89, "low": 55},
                { "date": "07 Oct 2018 00:00:00 GMT-6", "average": 77, "high": 100, "low": 31},
                { "date": "08 Oct 2018 00:00:00 GMT-6", "average": 79, "high": 89, "low": 54},
                { "date": "09 Oct 2018 00:00:00 GMT-6", "average": 72, "high": 94, "low": 57},
                { "date": "10 Oct 2018 00:00:00 GMT-6", "average": 79, "high": 90, "low": 32},
                { "date": "11 Oct 2018 00:00:00 GMT-6", "average": 82, "high": 93, "low": 22},
                { "date": "12 Oct 2018 00:00:00 GMT-6", "average": 83, "high": 97, "low": 33},
                { "date": "13 Oct 2018 00:00:00 GMT-6", "average": 88, "high": 97, "low": 13},
                { "date": "14 Oct 2018 00:00:00 GMT-6", "average": 81, "high": 86, "low": 48},
                { "date": "15 Oct 2018 00:00:00 GMT-6", "average": 90, "high": 86, "low": 53},
                { "date": "16 Oct 2018 00:00:00 GMT-6", "average": 89, "high": 96, "low": 33},
                { "date": "17 Oct 2018 00:00:00 GMT-6", "average": 75, "high": 92, "low": 15},
                { "date": "18 Oct 2018 00:00:00 GMT-6", "average": 87, "high": 95, "low": 6},
                { "date": "19 Oct 2018 00:00:00 GMT-6", "average": 72, "high": 96, "low": 38},
                { "date": "20 Oct 2018 00:00:00 GMT-6", "average": 85, "high": 98, "low": 9},
                { "date": "21 Oct 2018 00:00:00 GMT-6", "average": 82, "high": 87, "low": 30},
                { "date": "22 Oct 2018 00:00:00 GMT-6", "average": 87, "high": 93, "low": 51},
                { "date": "23 Oct 2018 00:00:00 GMT-6", "average": 83, "high": 93, "low": 42},
                { "date": "24 Oct 2018 00:00:00 GMT-6", "average": 78, "high": 94, "low": 29},
                { "date": "25 Oct 2018 00:00:00 GMT-6", "average": 82, "high": 87, "low": 15},
                { "date": "26 Oct 2018 00:00:00 GMT-6", "average": 73, "high": 90, "low": 43},
                { "date": "27 Oct 2018 00:00:00 GMT-6", "average": 82, "high": 96, "low": 13},
                { "date": "28 Oct 2018 00:00:00 GMT-6", "average": 70, "high": 98, "low": 39},
                { "date": "29 Oct 2018 00:00:00 GMT-6", "average": 86, "high": 90, "low": 56},
                { "date": "30 Oct 2018 00:00:00 GMT-6", "average": 84, "high": 88, "low": 56},
                { "date": "31 Oct 2018 00:00:00 GMT-6", "average": 82, "high": 85, "low": 52},
                { "date": "01 Nov 2018 00:00:00 GMT-6", "average": 75, "high": 92, "low": 22},
                { "date": "02 Nov 2018 00:00:00 GMT-6", "average": 82, "high": 99, "low": 11},
                { "date": "03 Nov 2018 00:00:00 GMT-6", "average": 86, "high": 94, "low": 9},
                { "date": "04 Nov 2018 00:00:00 GMT-6", "average": 90, "high": 87, "low": 45},
                { "date": "05 Nov 2018 00:00:00 GMT-6", "average": 74, "high": 95, "low": 37},
                { "date": "06 Nov 2018 00:00:00 GMT-6", "average": 81, "high": 89, "low": 41},
                { "date": "07 Nov 2018 00:00:00 GMT-6", "average": 86, "high": 96, "low": 25},
                { "date": "08 Nov 2018 00:00:00 GMT-6", "average": 83, "high": 95, "low": 27},
                { "date": "09 Nov 2018 00:00:00 GMT-6", "average": 81, "high": 86, "low": 15},
                { "date": "10 Nov 2018 00:00:00 GMT-6", "average": 83, "high": 95, "low": 3},
                { "date": "11 Nov 2018 00:00:00 GMT-6", "average": 89, "high": 94, "low": 60},
                { "date": "12 Nov 2018 00:00:00 GMT-6", "average": 84, "high": 85, "low": 20},
                { "date": "13 Nov 2018 00:00:00 GMT-6", "average": 87, "high": 97, "low": 26},
                { "date": "14 Nov 2018 00:00:00 GMT-6", "average": 72, "high": 100, "low": 15},
                { "date": "15 Nov 2018 00:00:00 GMT-6", "average": 71, "high": 98, "low": 10},
                { "date": "16 Nov 2018 00:00:00 GMT-6", "average": 80, "high": 97, "low": 3},
                { "date": "17 Nov 2018 00:00:00 GMT-6", "average": 81, "high": 90, "low": 57},
                { "date": "18 Nov 2018 00:00:00 GMT-6", "average": 72, "high": 91, "low": 17},
                { "date": "19 Nov 2018 00:00:00 GMT-6", "average": 73, "high": 95, "low": 16},
                { "date": "20 Nov 2018 00:00:00 GMT-6", "average": 77, "high": 87, "low": 48},
                { "date": "21 Nov 2018 00:00:00 GMT-6", "average": 78, "high": 99, "low": 16},
                { "date": "22 Nov 2018 00:00:00 GMT-6", "average": 84, "high": 87, "low": 16},
                { "date": "23 Nov 2018 00:00:00 GMT-6", "average": 72, "high": 87, "low": 31},
                { "date": "24 Nov 2018 00:00:00 GMT-6", "average": 89, "high": 90, "low": 29},
                { "date": "25 Nov 2018 00:00:00 GMT-6", "average": 80, "high": 88, "low": 47},
                { "date": "26 Nov 2018 00:00:00 GMT-6", "average": 86, "high": 91, "low": 9},
                { "date": "27 Nov 2018 00:00:00 GMT-6", "average": 72, "high": 88, "low": 18},
                { "date": "28 Nov 2018 00:00:00 GMT-6", "average": 89, "high": 87, "low": 40},
                { "date": "29 Nov 2018 00:00:00 GMT-6", "average": 81, "high": 92, "low": 1},
                { "date": "30 Nov 2018 00:00:00 GMT-6", "average": 78, "high": 88, "low": 51},
                { "date": "01 Dec 2018 00:00:00 GMT-6", "average": 71, "high": 85, "low": 9},
                { "date": "02 Dec 2018 00:00:00 GMT-6", "average": 87, "high": 92, "low": 42},
                { "date": "03 Dec 2018 00:00:00 GMT-6", "average": 80, "high": 99, "low": 44},
                { "date": "04 Dec 2018 00:00:00 GMT-6", "average": 76, "high": 99, "low": 49},
                { "date": "05 Dec 2018 00:00:00 GMT-6", "average": 88, "high": 91, "low": 60},
                { "date": "06 Dec 2018 00:00:00 GMT-6", "average": 73, "high": 87, "low": 13},
                { "date": "07 Dec 2018 00:00:00 GMT-6", "average": 71, "high": 100, "low": 22},
                { "date": "08 Dec 2018 00:00:00 GMT-6", "average": 89, "high": 91, "low": 38},
                { "date": "09 Dec 2018 00:00:00 GMT-6", "average": 73, "high": 86, "low": 56},
                { "date": "10 Dec 2018 00:00:00 GMT-6", "average": 80, "high": 86, "low": 29},
                { "date": "11 Dec 2018 00:00:00 GMT-6", "average": 75, "high": 97, "low": 56},
                { "date": "12 Dec 2018 00:00:00 GMT-6", "average": 72, "high": 92, "low": 33},
                { "date": "13 Dec 2018 00:00:00 GMT-6", "average": 79, "high": 85, "low": 45},
                { "date": "14 Dec 2018 00:00:00 GMT-6", "average": 74, "high": 93, "low": 24},
                { "date": "15 Dec 2018 00:00:00 GMT-6", "average": 86, "high": 87, "low": 38},
                { "date": "16 Dec 2018 00:00:00 GMT-6", "average": 74, "high": 94, "low": 15},
                { "date": "17 Dec 2018 00:00:00 GMT-6", "average": 82, "high": 90, "low": 44},
                { "date": "18 Dec 2018 00:00:00 GMT-6", "average": 85, "high": 90, "low": 25},
                { "date": "19 Dec 2018 00:00:00 GMT-6", "average": 75, "high": 100, "low": 21},
                { "date": "20 Dec 2018 00:00:00 GMT-6", "average": 89, "high": 100, "low": 14},
                { "date": "21 Dec 2018 00:00:00 GMT-6", "average": 70, "high": 91, "low": 54},
                { "date": "22 Dec 2018 00:00:00 GMT-6", "average": 72, "high": 90, "low": 25},
                { "date": "23 Dec 2018 00:00:00 GMT-6", "average": 84, "high": 87, "low": 52},
                { "date": "24 Dec 2018 00:00:00 GMT-6", "average": 80, "high": 98, "low": 34},
                { "date": "25 Dec 2018 00:00:00 GMT-6", "average": 81, "high": 99, "low": 5},
                { "date": "26 Dec 2018 00:00:00 GMT-6", "average": 77, "high": 88, "low": 5},
                { "date": "27 Dec 2018 00:00:00 GMT-6", "average": 83, "high": 89, "low": 23},
                { "date": "28 Dec 2018 00:00:00 GMT-6", "average": 87, "high": 96, "low": 27},
                { "date": "29 Dec 2018 00:00:00 GMT-6", "average": 89, "high": 91, "low": 36},
                { "date": "30 Dec 2018 00:00:00 GMT-6", "average": 76, "high": 98, "low": 25},
                { "date": "31 Dec 2018 00:00:00 GMT-6", "average": 89, "high": 90, "low": 17},
                { "date": "01 Jan 2019 00:00:00 GMT-6", "average": 73, "high": 88, "low": 22},
                { "date": "02 Jan 2019 00:00:00 GMT-6", "average": 78, "high": 87, "low": 35},
                { "date": "03 Jan 2019 00:00:00 GMT-6", "average": 70, "high": 91, "low": 57},
                { "date": "04 Jan 2019 00:00:00 GMT-6", "average": 82, "high": 94, "low": 26},
                { "date": "05 Jan 2019 00:00:00 GMT-6", "average": 78, "high": 93, "low": 13},
                { "date": "06 Jan 2019 00:00:00 GMT-6", "average": 88, "high": 87, "low": 37},
                { "date": "07 Jan 2019 00:00:00 GMT-6", "average": 82, "high": 95, "low": 28},
                { "date": "08 Jan 2019 00:00:00 GMT-6", "average": 78, "high": 99, "low": 3},
                { "date": "09 Jan 2019 00:00:00 GMT-6", "average": 84, "high": 98, "low": 2},
                { "date": "10 Jan 2019 00:00:00 GMT-6", "average": 79, "high": 100, "low": 30},
                { "date": "11 Jan 2019 00:00:00 GMT-6", "average": 84, "high": 97, "low": 9},
                { "date": "12 Jan 2019 00:00:00 GMT-6", "average": 71, "high": 100, "low": 26},
                { "date": "13 Jan 2019 00:00:00 GMT-6", "average": 76, "high": 91, "low": 40},
                { "date": "14 Jan 2019 00:00:00 GMT-6", "average": 88, "high": 90, "low": 24},
                { "date": "15 Jan 2019 00:00:00 GMT-6", "average": 79, "high": 95, "low": 46},
                { "date": "16 Jan 2019 00:00:00 GMT-6", "average": 73, "high": 87, "low": 30},
                { "date": "17 Jan 2019 00:00:00 GMT-6", "average": 79, "high": 89, "low": 57},
                { "date": "18 Jan 2019 00:00:00 GMT-6", "average": 74, "high": 100, "low": 34},
                { "date": "19 Jan 2019 00:00:00 GMT-6", "average": 76, "high": 97, "low": 56},
                { "date": "20 Jan 2019 00:00:00 GMT-6", "average": 89, "high": 88, "low": 46},
                { "date": "21 Jan 2019 00:00:00 GMT-6", "average": 80, "high": 87, "low": 4},
                { "date": "22 Jan 2019 00:00:00 GMT-6", "average": 74, "high": 87, "low": 24},
                { "date": "23 Jan 2019 00:00:00 GMT-6", "average": 88, "high": 88, "low": 24},
                { "date": "24 Jan 2019 00:00:00 GMT-6", "average": 75, "high": 90, "low": 4},
                { "date": "25 Jan 2019 00:00:00 GMT-6", "average": 87, "high": 85, "low": 52},
                { "date": "26 Jan 2019 00:00:00 GMT-6", "average": 81, "high": 93, "low": 55},
                { "date": "27 Jan 2019 00:00:00 GMT-6", "average": 86, "high": 97, "low": 39},
                { "date": "28 Jan 2019 00:00:00 GMT-6", "average": 82, "high": 91, "low": 1},
                { "date": "29 Jan 2019 00:00:00 GMT-6", "average": 74, "high": 91, "low": 59},
                { "date": "30 Jan 2019 00:00:00 GMT-6", "average": 76, "high": 86, "low": 37},
                { "date": "31 Jan 2019 00:00:00 GMT-6", "average": 79, "high": 87, "low": 42},
                { "date": "01 Feb 2019 00:00:00 GMT-6", "average": 70, "high": 89, "low": 60},
                { "date": "02 Feb 2019 00:00:00 GMT-6", "average": 71, "high": 90, "low": 35},
                { "date": "03 Feb 2019 00:00:00 GMT-6", "average": 83, "high": 90, "low": 15},
                { "date": "04 Feb 2019 00:00:00 GMT-6", "average": 77, "high": 95, "low": 55},
                { "date": "05 Feb 2019 00:00:00 GMT-6", "average": 89, "high": 89, "low": 43},
                { "date": "06 Feb 2019 00:00:00 GMT-6", "average": 90, "high": 94, "low": 44},
                { "date": "07 Feb 2019 00:00:00 GMT-6", "average": 71, "high": 96, "low": 20},
                { "date": "08 Feb 2019 00:00:00 GMT-6", "average": 75, "high": 100, "low": 28},
                { "date": "09 Feb 2019 00:00:00 GMT-6", "average": 70, "high": 97, "low": 42},
                { "date": "10 Feb 2019 00:00:00 GMT-6", "average": 85, "high": 93, "low": 59},
                { "date": "11 Feb 2019 00:00:00 GMT-6", "average": 76, "high": 86, "low": 30},
                { "date": "12 Feb 2019 00:00:00 GMT-6", "average": 89, "high": 99, "low": 44},
                { "date": "13 Feb 2019 00:00:00 GMT-6", "average": 81, "high": 90, "low": 22},
                { "date": "14 Feb 2019 00:00:00 GMT-6", "average": 79, "high": 100, "low": 47},
                { "date": "15 Feb 2019 00:00:00 GMT-6", "average": 71, "high": 87, "low": 27},
                { "date": "16 Feb 2019 00:00:00 GMT-6", "average": 86, "high": 98, "low": 4},
                { "date": "17 Feb 2019 00:00:00 GMT-6", "average": 79, "high": 100, "low": 58},
                { "date": "18 Feb 2019 00:00:00 GMT-6", "average": 73, "high": 98, "low": 1},
                { "date": "19 Feb 2019 00:00:00 GMT-6", "average": 70, "high": 96, "low": 23},
                { "date": "20 Feb 2019 00:00:00 GMT-6", "average": 88, "high": 86, "low": 12},
                { "date": "21 Feb 2019 00:00:00 GMT-6", "average": 86, "high": 100, "low": 5},
                { "date": "22 Feb 2019 00:00:00 GMT-6", "average": 80, "high": 92, "low": 53},
                { "date": "23 Feb 2019 00:00:00 GMT-6", "average": 87, "high": 87, "low": 0},
                { "date": "24 Feb 2019 00:00:00 GMT-6", "average": 74, "high": 94, "low": 47},
                { "date": "25 Feb 2019 00:00:00 GMT-6", "average": 77, "high": 96, "low": 27},
                { "date": "26 Feb 2019 00:00:00 GMT-6", "average": 89, "high": 91, "low": 14},
                { "date": "27 Feb 2019 00:00:00 GMT-6", "average": 76, "high": 100, "low": 14},
                { "date": "28 Feb 2019 00:00:00 GMT-6", "average": 80, "high": 100, "low": 37},
                { "date": "01 Mar 2019 00:00:00 GMT-6", "average": 83, "high": 85, "low": 26},
                { "date": "02 Mar 2019 00:00:00 GMT-6", "average": 88, "high": 98, "low": 33},
                { "date": "03 Mar 2019 00:00:00 GMT-6", "average": 78, "high": 94, "low": 24},
                { "date": "04 Mar 2019 00:00:00 GMT-6", "average": 82, "high": 91, "low": 6},
                { "date": "05 Mar 2019 00:00:00 GMT-6", "average": 86, "high": 100, "low": 59},
                { "date": "06 Mar 2019 00:00:00 GMT-6", "average": 89, "high": 100, "low": 26},
                { "date": "07 Mar 2019 00:00:00 GMT-6", "average": 79, "high": 95, "low": 47},
                { "date": "08 Mar 2019 00:00:00 GMT-6", "average": 70, "high": 92, "low": 33},
                { "date": "09 Mar 2019 00:00:00 GMT-6", "average": 86, "high": 99, "low": 60},
                { "date": "10 Mar 2019 00:00:00 GMT-6", "average": 85, "high": 88, "low": 59},
                { "date": "11 Mar 2019 00:00:00 GMT-6", "average": 89, "high": 99, "low": 60},
                { "date": "12 Mar 2019 00:00:00 GMT-6", "average": 71, "high": 90, "low": 28},
                { "date": "13 Mar 2019 00:00:00 GMT-6", "average": 77, "high": 89, "low": 41},
                { "date": "14 Mar 2019 00:00:00 GMT-6", "average": 73, "high": 85, "low": 22},
                { "date": "15 Mar 2019 00:00:00 GMT-6", "average": 83, "high": 85, "low": 35},
                { "date": "16 Mar 2019 00:00:00 GMT-6", "average": 77, "high": 94, "low": 6},
                { "date": "17 Mar 2019 00:00:00 GMT-6", "average": 90, "high": 89, "low": 19},
                { "date": "18 Mar 2019 00:00:00 GMT-6", "average": 85, "high": 100, "low": 12},
                { "date": "19 Mar 2019 00:00:00 GMT-6", "average": 84, "high": 94, "low": 60},
                { "date": "20 Mar 2019 00:00:00 GMT-6", "average": 83, "high": 90, "low": 50},
                { "date": "21 Mar 2019 00:00:00 GMT-6", "average": 87, "high": 92, "low": 39},
                { "date": "22 Mar 2019 00:00:00 GMT-6", "average": 74, "high": 95, "low": 30},
                { "date": "23 Mar 2019 00:00:00 GMT-6", "average": 90, "high": 90, "low": 40},
                { "date": "24 Mar 2019 00:00:00 GMT-6", "average": 90, "high": 88, "low": 42},
                { "date": "25 Mar 2019 00:00:00 GMT-6", "average": 83, "high": 85, "low": 14},
                { "date": "26 Mar 2019 00:00:00 GMT-6", "average": 81, "high": 98, "low": 2},
                { "date": "27 Mar 2019 00:00:00 GMT-6", "average": 71, "high": 92, "low": 27},
                { "date": "28 Mar 2019 00:00:00 GMT-6", "average": 81, "high": 87, "low": 45},
                { "date": "29 Mar 2019 00:00:00 GMT-6", "average": 79, "high": 88, "low": 13},
                { "date": "30 Mar 2019 00:00:00 GMT-6", "average": 86, "high": 85, "low": 11},
                { "date": "31 Mar 2019 00:00:00 GMT-6", "average": 87, "high": 100, "low": 56},
                { "date": "01 Apr 2019 00:00:00 GMT-6", "average": 86, "high": 95, "low": 54},
                { "date": "02 Apr 2019 00:00:00 GMT-6", "average": 74, "high": 88, "low": 19}
            ]
            }];
            for (var i = 0; i < data[0].values.length; i++) {
                var pd = Date.parse(data[0].values[i].date);
                data[0].values[i].date = pd;
            }
            this.data = data;
        }

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
