import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    selected_items: [],
    th: [],
    ROBOT_HEALTH: [],
    CURRENT_DATA: [],
    TEMPERATURE_DATA: [],
    ALL_ROBOT_HEALTH: []
  },
  getters: {

  },
  actions: {

  },
  mutations: {
    updateSelectedItems(state, newItems) {
      state.selected_items = newItems;
    },
    updateTh(state, newTh) {
      state.th = newTh;
    },
    pushRobotHealth(state, newItem) {
      state.ROBOT_HEALTH.push(newItem);
    },
    pushCurrentData(state, newItem){
      state.CURRENT_DATA.push(newItem);
    },
    pushTemperatureData(state, newItem) {
      state.TEMPERATURE_DATA.push(newItem);
    },
    pushAllRobotHealth(state, newItem) {
      state.ALL_ROBOT_HEALTH.push(newItem);
    },
    clearRobotHealth(state) {
      state.ROBOT_HEALTH = [];
    },
    clearCurrentData(state){
      state.CURRENT_DATA = [];
    },
    clearTemperatureData(state) {
      state.TEMPERATURE_DATA = [];
    },
    clearAllRobotHealth(state) {
      state.ALL_ROBOT_HEALTH = [];
    }
  }
})
