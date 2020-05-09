<template>
  <q-page class="BRAND__page-content">
    <h1>{{ content.heading }}</h1>
    <StreamField v-for="(stream_field, index) in content.stream_fields" v-bind="stream_field" :key="str_id + index">
    </StreamField>
    <p v-if="app.app_debug">site_configuration {{ app.site_configuration }}</p>
    <div class="row">
      <div class="col-sm-12 col-md-9">
        blogs list
        blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah
        <ul id="blogs">
          <li v-for="item in blogs" :key="item.str_id">
            <router-link :to="blogPrefixLink + '/' + item.id.slug">{{ item.id.slug }}</router-link>
          </li>
        </ul>
      </div>
      <div class="col-3">
      blogs archives janvier février février février février février février février février février février février février février février février février février février février février février février février février février février février février février février février février février février février
      </div>
    </div>
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
