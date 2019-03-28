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
export default {
  name: 'RobotHealth',
  data () {
    return {
      msg: 'no msg'
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
