/* eslint-disable-next-line import/no-extraneous-dependencies */
import Vue from 'vue'
/* eslint-disable-next-line import/no-extraneous-dependencies */
import Buefy from 'buefy'
/* eslint-disable-next-line import/no-extraneous-dependencies */
import { faCog } from '@fortawesome/free-solid-svg-icons'
/* eslint-disable-next-line import/no-extraneous-dependencies */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
/* eslint-disable-next-line import/no-extraneous-dependencies */
import { library } from '@fortawesome/fontawesome-svg-core'
import App from './App'
import router from './router'
import store from './store'

/* eslint-disable-next-line import/no-extraneous-dependencies */
import 'bulma/css/bulma.css'

// enables Buefy
Vue.use(Buefy)

// Font Awesome settings
library.add(faCog)
Vue.component('font-awesome-icon', FontAwesomeIcon)

/* eslint-disable-next-line no-new */
new Vue({
  el: '#app',
  store,
  router,
  // the template compiler of Vue can be omitted
  // by implementing the render function yourself
  render: h => h(App),
  mounted () {
    console.log('main.js: mounted')
  }
})
