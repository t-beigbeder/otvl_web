<template>
  <q-page class="BRAND__page-content">
    <div class="row">
      <div class="col-12 col-md-9 q-pr-md-sm">
        <h1>{{ content.heading }}</h1>
        <StreamField v-for="(stream_field, index) in content.stream_fields" v-bind="stream_field" :key="str_id + index">
        </StreamField>
        <p v-if="app.app_debug">site_configuration {{ app.site_configuration }}</p>
        <p>blogs list
        blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah blah
        </p>
        <ul id="blogs">
          <li v-for="item in blogs" :key="item.str_id">
            <router-link :to="blogPrefixLink + '/' + item.id.slug">{{ item.id.slug }}</router-link>
          </li>
        </ul>
      </div>
      <div class="col-12 col-md-3 q-pl-md-sm">
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
  },
  methods: {
    fetchBlogIndex: function () {
      this.type = this.$route.path.split('/')[1]
      this.id.section = this.$route.params.section
      this.id.sub_section = this.$route.params.sub_section || ''
      this.id.slug = this.$route.params.slug || ''
      if (this.app.app_debug_console) {
        console.log(`fetchBlogIndex str_id ${this.str_id} type ${this.type}`)
      }

      if (this.app.app_debug_simul_rest) {
        this.simulFetchBlogIndex()
      } else {
        this.$axios.get(`http://dxpydk:8888/blogs/${this.str_id}/`)
          .then((response) => {
            if (this.app.app_debug_console) {
              console.log(`fetchBlogIndex str_id ${this.str_id} response data`)
              console.log(response.data)
            }
          })
          .catch((error) => {
            if (error.response && error.response.status === 404) {
              this.$router.push('/404')
            } else {
              this.$router.push('/err')
            }
          })
      }
    }
  }
}
</script>
