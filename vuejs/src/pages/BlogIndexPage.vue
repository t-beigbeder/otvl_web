<template>
  <q-page class="BRAND__page-content">
    <div class="row">
      <div class="col-12 col-md-9 q-pr-md-sm">
        <h1>{{ content.heading }}</h1>
        <StreamField v-for="(stream_field, index) in content.stream_fields" v-bind="stream_field" :key="str_id + index">
        </StreamField>
        <p v-if="app.app_debug">site_configuration {{ app.site_configuration }}</p>
        <q-separator spaced />
        <div v-for="blog in blogs" :key="blog.slug" class="row q-pl-md">
          <h2 class="col-12 col-md-9">{{ blog.heading }}</h2>
          <p class="col-12 col-md-3 q-my-auto text-caption">
            Published on: {{ blog.publication_date }}
          </p>
          <div class="col-12">
            {{ blog.summary }}
            <q-btn class="q-ml-md" dense color="blue-grey-2" text-color="blue-grey-9" no-caps :to="blogPrefixLink + '/' + blog.slug" :label="content.brand.labels.blog_index_read_more"></q-btn>
          </div>
          <q-separator spaced class="col-12" />
        </div>

      </div>
      <div class="col-3 q-mt-xl q-pl-md-sm">
        <BlogBrowser :app="app" :brand="content.brand" :index_url="content.index_url"></BlogBrowser>
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
        this.$axios.get(`${this.app.rtc.api_server_url}/blogs/${this.str_id}/`)
          .then((response) => {
            if (this.app.app_debug_console) {
              console.log(`fetchBlogIndex str_id ${this.str_id}`)
            }
            this.$set(this, 'blogs', response.data.blogs)
          })
          .catch((error) => {
            if (error.response && error.response.status === 404) {
              location.replace(`${this.app.rtc.web_server_url}/statics/error/page_not_found.html`)
            } else {
              location.replace(`${this.app.rtc.web_server_url}/statics/error/technical_error.html`)
            }
          })
      }
    }
  }
}
</script>
