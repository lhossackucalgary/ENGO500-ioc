<template>
  <div class="">
    <h2>Selected Items</h2>
    <button name="button">Compare!</button>
    <ul>
      <li
        is="selected-item"
        v-for="(item, index) in selected"
        v-bind:key="index.iotid"
        v-bind:feature="item"
        v-on:remove="selected.splice(index, 1)"
      ></li>
    </ul>
  </div>
</template>

<script>
import SelectedItem from './SelectedItem.vue';

export default {
  components: {
    'selected-item': SelectedItem
  },
  created(){
      let localThis = this
      document.addEventListener('addbotcmp', this.addBotCmp)
  },
  data() {
    return {
      selected: []
    }
  },
  methods: {
    addBotCmp:function(e) {
      let inSet = false;
      for (let i = 0; i < this.selected.length; i++) {
        if (e.detail.iotid === this.selected[i].iotid){
          inSet = true;
        }
      }
      if (!inSet) {
        this.selected.push(e.detail);
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
  margin-bottom: 0px;
}
ul {
  list-style-type: none;
  padding: 0;
  border-top: 1px solid black;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
