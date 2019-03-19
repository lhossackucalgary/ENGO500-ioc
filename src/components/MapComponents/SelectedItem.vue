<template>
  <li>
    <div>
      Name: {{feature.name}} <br>
      Iot Id: {{feature.iotid}} <br>
      Status: {{feature.properties.status}} <br>
      <button v-on:click="$emit('remove')">x</button>
    </div>
  </li>
</template>

<script>
export default {
  props: {
    feature: Object
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
button {
  position: relative;
}
li {
  display: inline-block;
  margin: 0 0px;
  width: 100%;
  border-bottom: 1px solid black;
}
a {
  color: #42b983;
}
</style>
