/* eslint-disable import/no-extraneous-dependencies */
import Vue from 'vue'
import Router from 'vue-router'
import VideoCapture from '@/components/VideoCapture'

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'home',
    component: VideoCapture
  }
]

export default new Router({
  routes
})
