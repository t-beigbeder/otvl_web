<template>
  <q-layout class="BRAND__page-content">
    <h1>{{ content.heading }}</h1>
    <StreamField v-for="(stream_field, index) in content.stream_fields" v-bind="stream_field" :key="str_id + index">
    </StreamField>
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
