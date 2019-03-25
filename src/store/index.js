import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    selected_items: []
  },
  getters: {

  },
  actions: {

  },
  mutations: {
    updateSelectedItems (state, newItems) {
      state.selected_items = newItems;
    }
  }
})
