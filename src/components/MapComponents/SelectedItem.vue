<template>
  <li class="">
    Name: {{feature.name}} <br>
    Iot Id: {{feature.iotid}} <br>
    Status: {{feature.properties.status}} <br>

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
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
