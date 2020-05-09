<template>
  <q-page class="BRAND__page-content">
    <h1>{{ content.heading }}</h1>
    <StreamField v-for="(stream_field, index) in content.stream_fields" v-bind="stream_field" :key="str_id + index">
    </StreamField>
    <p v-if="app.app_debug">site_configuration {{ app.site_configuration }}</p>
    beforer ul
    <ul id="blogs">
      <li v-for="item in blogs" :key="item.str_id">
        <router-link :to="blogPrefixLink + '/' + item.id.slug">{{ item.id.slug }}</router-link>
      </li>
    </ul>
  </q-page>
</template>

<script>
import PageMixin from '../mixins/PageMixin'

export default {
  mixins: [PageMixin],
  name: 'BlogIndexPage',
  data: function () {
    return {
      blogs: function () {
        return []
      }
    }
  },
  computed: {
    blogPrefixLink: function () {
      const page = this.getPageById(this.str_id)
      return (this.id.sub_section ? `/${page.blog_type}/${this.id.section}/${this.id.sub_section}` : `/${page.blog_type}/${this.id.section}`)
    }
  }
}
</script>
