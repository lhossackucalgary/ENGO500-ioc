<template>
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
</template>

<script>
/* constants */
const WIDTH = 1000; //800
const HEIGHT = 300; //100
const PAD = 10;
const MARGIN = 50;
const _margin = ({top: 10, right: 0, bottom: 30, left: 40});
const PADDING_FOR_LABELS = 90;


export default {
  name: 'RobotHealth',
  data () {
    return {
      _vis1: []
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
            this._vis1.width = this._vis1.svg.node().getBoundingClientRect().width != undefined ?
                this._vis1.svg.node().getBoundingClientRect().width : this._vis1.width; //if undefined
            this._vis1.height = this._vis1.svg.node().getBoundingClientRect().height;

            this._vis1.data = this.$store.state.ROBOT_HEALTH;
            this._vis1.setupScales([this._vis1.height - _margin.bottom, _margin.top], [0, 100], [0, this._vis1.width - _margin.left], this._vis1.data.length);
            this._vis1.setupAxis();
            this._vis1.createBars();
        } else {
            setTimeout(this.setupVis1, 500);
        }
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
</style>
