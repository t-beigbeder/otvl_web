<template>
  <q-layout class="BRAND__page-content">
    <h1>{{ content.heading }}</h1>
    <span v-html="content.html"></span>
    <p v-if="app.app_debug">site_configuration {{ app.site_configuration }}</p>

    <q-page-container>
      <router-view></router-view>
    </q-page-container>
  </q-layout>
</template>

<script>
import PageMixin from '../mixins/PageMixin'

export default {
  mixins: [PageMixin],
  name: 'StandardPage'
}
</script>
