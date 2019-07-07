<template>
  <div class='container'>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'app',
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
