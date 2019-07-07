<template>
  <div>
    <h1>{{ title }}</h1>
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
