<template>
  <q-layout>
    <h4>{{ content.heading }}</h4>
    <p>This is a standard page.</p>
    <p>The section is {{ $route.params.section }}</p>
    <p>The sub_section is {{ $route.params.sub_section }}</p>
    <p>The slug is {{ $route.params.slug }}</p>
    <p>The str_id is {{ str_id }}</p>

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
