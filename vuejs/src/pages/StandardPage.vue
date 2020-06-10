<template>
  <q-page class="BRAND__page-content page-article">
    <h1>{{ content.heading }}</h1>
    <StreamField v-for="(stream_field, index) in content.stream_fields" v-bind="stream_field" :key="str_id + index" :meta="meta" :brand="content.brand">
    </StreamField>
    <p v-if="app.app_debug">site_configuration {{ app.site_configuration }}</p>
  </q-page>
</template>

<script>
import PageMixin from '../mixins/PageMixin'

export default {
  mixins: [PageMixin],
  name: 'StandardPage'
}
</script>
