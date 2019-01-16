<template>
  <div class="">
    <h2>Map Layers</h2>
    <ul>
      <li>Robot
        <ul>
          <li>High Priority</li>
          <li>Medium Priority</li>
          <li>Low Priority</li>
          <li>Name</li>
        </ul>
      </li>
      <li>Maintenance Crew
        <ul>
          <li>Name</li>
        </ul>
      </li>
      <li>Route
        <ul>
          <li>Confirmed</li>
          <li>Pending</li>
        </ul>
      </li>
    </ul>
    <hr>
  </div>
</template>

<script>
export default {

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding-left: 30px;
  text-align: left;
}
a {
  color: #42b983;
}
</style>
