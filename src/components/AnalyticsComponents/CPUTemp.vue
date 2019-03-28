<template>
  <div>
      <div id="vis3box" class="vis_div">
          <h3>Sensor876: CPU Temperature</h3>
          <svg id="vis3" class="svg_boxes"></svg>
      </div>
      <div id="vis3btn" class="vis_btn">
          <p>Enter list of robot names: </p>
          <textarea id="vis3textbox" v-model="message_v3" placeholder="robot1 robot2 ..."></textarea>
          <br>
          <button id="btn_vis3_update" class="cat" v-on:click="vis3_update()">Update Chart</button>
      </div>
  </div>

</template>

<script>
export default {
  name: 'CPUTemp',
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
