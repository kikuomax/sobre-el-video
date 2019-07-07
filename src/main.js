'use strict'

import App from './App'
import Vue from 'vue'

new Vue({
  el: '#app',
  // the template compiler of Vue can be omitted
  // by implementing the render function yourself
  render: h => h(App),
  mounted () {
    console.log('main.js: mounted')
  }
})
