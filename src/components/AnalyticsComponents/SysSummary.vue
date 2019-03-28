<template>
  <div>
      <h3>Robot Summary</h3>
      <div id="vis7" class="vis_div"></div>
  </div>
</template>

<script>
import * as vega from 'vega'
import {default as vegaEmbed} from 'vega-embed'
import * as vegaLite from 'vega-lite'




export default {
  name: 'SysSummary',
  data () {
    return {
      _vis7data
    }
  },
  mounted() {
    this.setUpVis7();
  },
  methods: {
     setUpVis7() {
        var th = this.$store.state.th;
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

            this._vis7data = [{
                "name": "robots",
                "values": newData
            }]
            this.setupDotChart();
        } else {
            setTimeout(this.setUpVis7, 500)
        }
        },

    setupDotChart(){
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

        "data": this._vis7data,

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
