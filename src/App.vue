<template>
  <div class='container'>
    <app-header />
    <router-view />
  </div>
</template>

<script>
import AppHeader from './components/AppHeader'

export default {
  name: 'app',
  components: {
    AppHeader
  },
  data () {
    return {
      title: 'App'
    }
  },
  mounted () {
    console.log('App.vue: mounted')
  }
}
</script>

<style>
</style>
