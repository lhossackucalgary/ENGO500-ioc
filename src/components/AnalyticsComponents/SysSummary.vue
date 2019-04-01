<template>
  <div>
      <h2>System Summary</h2>
      <div id="vis7" class="vis_div"></div>
  </div>
</template>

<script>
import * as vega from 'vega'
import {default as vegaEmbed} from 'vega-embed'
import * as vegaLite from 'vega-lite'

var stat_colors = [];


export default {
  name: 'SysSummary',
  data () {
    return {
      _vis7data: [],
      _vis7count: []
    }
  },
  mounted() {
    this.setUpVis7();
  },
  methods: {
     setUpVis7() {
        var th = this.$store.state.th;
        var stat_exist = {
            "a": 0,
            "r1": 0,
            "r2": 0,
            "r3": 0,
            "r4": 0,
            "r5": 0
        };
        if (th.length > 0) {
            var newData = [];
            for (var i = 0; i < th.length; i++) {
                var name = th[i].name.slice(0,5);
                if (name == "robot") {
                    if (th[i].status == "Healthy") {
                        var stat = "R1 - Healthy";
                        stat_exist.r1++;
                    }
                    else if (th[i].status == "Warning") {
                        var stat = "R2 - Warning";
                        stat_exist.r2++;
                    }
                    else if (th[i].status == "Urgent") {
                        var stat = "R3 - Urgent";
                        stat_exist.r3++;
                    }
                    else if (th[i].status == "Unknown") {
                        var stat = "R4 - Unknown";
                        stat_exist.r4++;
                    }
                    else if (th[i].status == "Needs parts") {
                        var stat = "R5 - Needs Parts";
                        stat_exist.r5++;
                    }
                } else {
                    var stat = "Active Crews";
                    stat_exist.a++;
                }
                var entry = {
                        "robot" : th[i].name,
                        "id" : th[i].id,
                        "status" : stat
                    };
                newData.push(entry);
            }

            stat_colors = [];
            var stat_counter = [];
            if (stat_exist.a > 0) {
                stat_colors.push('#000000');
                stat_counter.push({"status": "Active Crews", "count": stat_exist.a});
            }
            if (stat_exist.r1 > 0) {
                stat_colors.push('#32D144');
                stat_counter.push({"status": "R1 - Healthy", "count": stat_exist.r1});
            }
            if (stat_exist.r2 > 0) {
                stat_colors.push('#FB7F28');
                stat_counter.push({"status": "R2 - Warning", "count": stat_exist.r2});
            }
            if (stat_exist.r3 > 0) {
                stat_colors.push('#EC1C24');
                stat_counter.push({"status": "R3 - Urgent", "count": stat_exist.r3});
            }
            if (stat_exist.r4 > 0) {
                stat_colors.push('#3F48CC');
                stat_counter.push({"status": "R4 - Unknown", "count": stat_exist.r4});
            }
            if (stat_exist.r5 > 0) {
                stat_colors.push('#585858');
                stat_counter.push({"status": "R5 - Needs Parts", "count": stat_exist.r5});
            }
            //console.log(stat_colors);
            this._vis7data = {
                "name": "robots",
                "values": newData
            }
            
            this._vis7count = {
                "name": "botcount",
                "values": stat_counter
            }

            this.setupDotChart();
        } else {
            setTimeout(this.setUpVis7, 500)
        }
        },

    setupDotChart(){
        vega.scheme('basic', stat_colors);

        var spec = {
        "$schema": "https://vega.github.io/schema/vega/v5.json",
        "width": 1000,
        "height": 500,
        "padding": {"left": 5, "right": 5, "top": 0, "bottom": 30},
        "autosize": "none",

        "signals": [
            { "name": "cx", "update": "width / 2" },
            { "name": "cy", "update": "height / 2" },
            { "name": "labelY", "update": "height - 10"},
            { "name": "radius", "value": 8, "bind": {"input": "range", "min": 2, "max": 15, "step": 1} },
            { "name": "collide", "value": 1},
            { "name": "gravityX", "value": 0.2},
            { "name": "gravityY", "value": 0.1},
            { "name": "static", "value": false}
        ],

        "data": [this._vis7data,this._vis7count],

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
            { "orient": "bottom", "scale": "xscale", "labelFontSize": 15 }
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
                "zindex": {"value": 0},
                "tooltip": {"signal": "{'Name': datum.robot, 'ID': datum.id}"}
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
            },
            {
            "type": "text",
            "from": {"data": "botcount"},
            "encode": {
                "update": {
                "x": {"scale": "xscale", "field": "status"},
                "dx": {"value": 80},
                "y": {"signal": "labelY"},
                "fill": {"value": "black"},
                "align": {"value": "center"},
                "baseline": {"value": "center"},
                "text": {"field": "count"},
                "fontSize": {"value":18}
                }
            }
            }
        ]
        }

        vegaEmbed('#vis7', spec).then(function(result) {

            // Access the Vega view instance (https://vega.github.io/vega/docs/api/view/) as result.view
        }).catch(console.error);
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
</style>
