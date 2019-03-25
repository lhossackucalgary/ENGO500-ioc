/* eslint-disable */
<template>
  <div class="">
    <h2>Compare Robots Page</h2>
    <p>{{$store.state.selected_items}}</p>
  </div>
</template>

<script>
export default {
  name: 'CompareBots',
  data () {
    return {

    }
  },
  mounted () {
    console.log(this.$store.state.selected_items);
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
