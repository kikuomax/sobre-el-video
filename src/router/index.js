/* eslint-disable-next-line import/no-extraneous-dependencies */
import Vue from 'vue'
/* eslint-disable-next-line import/no-extraneous-dependencies */
import Router from 'vue-router'
import Settings from '@/components/Settings'
import VideoCapture from '@/components/VideoCapture'

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'home',
    component: VideoCapture
  },
  {
    path: '/settings',
    name: 'settings',
    component: Settings
  }
]

export default new Router({
  routes
})
