/* eslint-disable-next-line import/no-extraneous-dependencies */
import Vue from 'vue'
/* eslint-disable-next-line import/no-extraneous-dependencies */
import Vuex from 'vuex'

Vue.use(Vuex)

/**
 * State of the root Store.
 *
 * Has the following fields,
 * - `apiBaseUrl`: {`string`}
 *   Base URL of the REST API for video management.
 */
const state = {
  apiBaseUrl: ''
}

/**
 * Mutations of the root Store.
 *
 * Has the following functions,
 * - `setApiBaseUrl`:
 *   Sets the base URL of the REST API for video management.
 *   Accepts a string.
 */
const mutations = {
  setApiBaseUrl (s, apiBaseUrl) {
    /* eslint-disable-next-line no-param-reassign */
    s.apiBaseUrl = apiBaseUrl
  }
}

const store = new Vuex.Store({
  state,
  mutations
})

export default store
