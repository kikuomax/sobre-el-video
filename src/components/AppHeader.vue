<template>
  <nav class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" @click="home">K</a>
      <!-- burger button -->
      <a
        role="button"
        class="navbar-burger"
        :class="menuStyle"
        aria-label="menu"
        aria-expanded="false"
        data-target="app-header"
        @click="toggleBurger"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div id="app-header" class="navbar-menu" :class="menuStyle">
      <div class="navbar-end">
        <div class="navbar-item">
          <a class="button is-secondary" @click="settings">
            <font-awesome-icon icon="cog" />
          </a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data () {
    return {
      // class bindings for the burger button and navbar-menu
      menuStyle: {
        'is-active': false
      }
    }
  },
  methods: {
    home () {
      this.$router.push({ name: 'home' })
    },
    settings () {
      this.$router.push({ name: 'settings' })
    },
    // toggles burger <--> cross
    toggleBurger () {
      const { menuStyle } = this
      menuStyle['is-active'] = !menuStyle['is-active']
    }
  }
}
</script>
