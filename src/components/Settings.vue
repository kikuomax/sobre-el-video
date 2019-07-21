<template>
  <div class="settings">
    <h3 class="title is-3">Settings</h3>
    <b-field horizontal label="API Base URL">
      <b-input
        name="api-base-url"
        placeholder="API Base URL"
        v-model="localApiBaseUrl"
      >
      </b-input>
    </b-field>
    <b-field horizontal>
      <p class="control">
        <button class="button is-primary" @click="applySettings">
          Apply
        </button>
      </p>
    </b-field>
  </div>
</template>

<script>
/* eslint-disable-next-line import/no-extraneous-dependencies */
import { mapMutations, mapState } from 'vuex'

export default {
  data () {
    return {
      // Store's apiBaseUrl (this.apiBaseUrl) is copied to localApiBaseUrl
      // to defer update until the "Apply" button is pressed
      localApiBaseUrl: ''
    }
  },
  computed: {
    ...mapState(['apiBaseUrl'])
  },
  watch: {
    apiBaseUrl (newUrl) {
      this.localApiBaseUrl = newUrl
    }
  },
  methods: {
    ...mapMutations(['setApiBaseUrl']),
    applySettings () {
      this.setApiBaseUrl(this.localApiBaseUrl)
    }
  },
  mounted () {
    this.localApiBaseUrl = this.apiBaseUrl
  }
}
</script>

<style>
.settings {
  text-align: center;
}
</style>
