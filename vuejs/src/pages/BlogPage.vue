<template>
  <q-page class="BRAND__page-content">
    <div class="row q-mx-sm-lg q-mx-md-xl q-mt-sm-lg">
      <div class="col-grow col-md-9 q-pr-md-sm page-article">
        <h1>{{ content.heading }}</h1>
        <StreamField v-for="(stream_field, index) in content.stream_fields" v-bind="stream_field" :key="str_id + index" :meta="meta" :brand="content.brand">
        </StreamField>
        <p v-if="app.app_debug">site_configuration {{ app.site_configuration }}</p>
      </div>
      <div class="col-md-3 col-sm-4 q-pl-md-sm">
        <h1></h1>
        <span></span>
        <BlogBrowser :app="app" :brand="content.brand" :index_url="content.index_url"></BlogBrowser>
      </div>
    </div>
    <PageBottom :app="app"></PageBottom>
  </q-page>
</template>

<script>
import PageMixin from '../mixins/PageMixin'
import BlogBrowser from 'src/components/BlogBrowser'

export default {
  mixins: [PageMixin],
  name: 'BlogPage',
  components: {
    BlogBrowser
  },
  data: function () {
    return {
      content: {
        index_url: '',
        brand: {
          labels: {
          }
        }
      }
    }
  }
}
</script>
