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
          <li v-for="item in blogs" :key="item.slug">
            <router-link :to="blogPrefixLink + '/' + item.slug">{{ item.slug }}</router-link>
          </li>
        </ul>
      </div>
      <div class="col-3 q-mt-lg q-pl-md-sm">
        <BlogBrowser :index_title="content.index_title" :index_url="content.index_url"></BlogBrowser>
      </div>
    </div>
  </q-page>
</template>

<script>
import PageMixin from '../mixins/PageMixin'
import BlogBrowser from 'src/components/BlogBrowser'

export default {
  mixins: [PageMixin],
  name: 'BlogIndexPage',
  components: {
    BlogBrowser
  },
  data: function () {
    return {
      blogs: function () {
        return []
      },
      content: {
        index_title: '',
        index_url: ''
      }
    }
  },
  computed: {
    blogPrefixLink: function () {
      const blogType = this.app.site_configuration.types[this.type].blog_type
      return (this.id.sub_section ? `/${blogType}/${this.id.section}/${this.id.sub_section}` : `/${blogType}/${this.id.section}`)
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
              console.log(`fetchBlogIndex str_id ${this.str_id}`)
              this.$set(this, 'blogs', response.data.blogs)
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
