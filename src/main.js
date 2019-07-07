/* eslint-disable import/no-extraneous-dependencies */
import Vue from 'vue'
import App from './App'
import router from './router'

import 'bulma/css/bulma.css'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  // the template compiler of Vue can be omitted
  // by implementing the render function yourself
  render: h => h(App),
  mounted () {
    console.log('main.js: mounted')
  }
})
