<template>
  <q-page class="BRAND__page-content">
    <div class="row">
      <div class="col-md-9 q-pr-md-sm page-article">
        <PageHeaderAndFooter :page="this" :app="app" is_header></PageHeaderAndFooter>
        <h1>{{ content.heading }}</h1>
        <StreamField v-for="(stream_field, index) in content.stream_fields" v-bind="stream_field" :key="str_id + index">
        </StreamField>
        <p v-if="app.app_debug">site_configuration {{ app.site_configuration }}</p>
        <q-separator spaced  size="2px" color="blue-grey-2"/>
        <div v-for="blog in published_blogs" :key="blog.slug" class="row q-pl-md">
          <h3 class="col-12 col-md-9">{{ blog.summary_heading }}</h3>
          <p class="col-12 col-md-3 q-my-auto text-caption">
            {{ content.brand.labels.published_on }} {{ intlDate(blog.publication_date, locale) }}
          </p>
          <div class="col-12">
            {{ blog.summary }}
            <q-btn class="q-ml-md" dense color="blue-grey-2" text-color="blue-grey-9" no-caps :to="blogPrefixLink + '/' + blog.slug" :label="content.brand.labels.read_more"></q-btn>
          </div>
          <q-separator spaced class="col-12" size="2px" color="blue-grey-2"/>
        </div>

      </div>
      <div class="col-md-3 col-sm-4 q-pl-md-sm">
        <div v-if="content.brand.promotion" class="col q-mt-xl">
          <BlogPromotion :app="app" :brand="content.brand" :preview_blogs="preview_blogs" :blog_prefix_link="blogPrefixLink"></BlogPromotion>
        </div>
        <div class="col q-mt-lg">
          <BlogBrowser :app="app" :brand="content.brand" :index_url="content.index_url"></BlogBrowser>
        </div>
      </div>
      <div class="col-md-9 q-pr-md-sm">
        <PageHeaderAndFooter :page="this" :app="app"></PageHeaderAndFooter>
      </div>
    </div>
  </q-page>
</template>

<script>
import PageMixin from '../mixins/PageMixin'
import BlogBrowser from 'src/components/BlogBrowser'
import BlogPromotion from 'src/components/BlogPromotion'

export default {
  mixins: [PageMixin],
  name: 'BlogIndexPage',
  components: {
    BlogBrowser,
    BlogPromotion
  },
  data: function () {
    return {
      blogs: [],
      content: {
        brand: {
          labels: {}
        },
        index_url: ''
      }
    }
  },
  computed: {
    published_blogs: function () {
      return this.blogs.filter(
        function (blog) {
          return (!('preview' in blog) || !blog.preview)
        }
      )
    },
    preview_blogs: function () {
      return this.blogs.filter(
        function (blog) {
          return (('preview' in blog) && blog.preview)
        }
      )
    },
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
</script>
