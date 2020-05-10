import AppUtilMixin from 'src/mixins/AppUtilMixin'
import StreamField from 'src/components/StreamField'

export default {
  mixins: [AppUtilMixin],

  components: {
    StreamField
  },

  data: function () {
    return {
      id: {
        section: '',
        sub_section: '',
        slug: ''
      },
      type: '',
      meta: {
        version: '',
        creation_date: '',
        publication_date: '',
        last_update_date: '',
        summary: [],
        authors: []
      },
      content: {
        title: '',
        heading: '',
        stream_fields: []
      },
      content_updated: false
    }
  },
  props: ['app'],
  created: function () {
    if (this.app.app_debug_console) {
      console.log('created')
    }
    this.fetchContent()
  },
  watch: {
    content_updated () {
      if (this.app.app_debug_console) {
        console.log('Page content_updated')
      }
      if (this.app.site_configuration.types[this.type].is_blog_index) {
        this.fetchBlogIndex()
      }
    },
    $route: function () {
      if (this.app.app_debug_console) {
        console.log('watch $route')
      }
      this.fetchContent()
    }
  },
  computed: {
    str_id: function () {
      return this.id.section + '/' + this.id.sub_section + '/' + this.id.slug
    }
  },
  methods: {
    simulFetchContent: function () {
      if (this.content.title) {
        document.title = this.content.title
      } else {
        // TODO: remove this test
        document.title = 'Title ' + this.id.section + ' ' + this.id.sub_section + ' ' + this.id.slug
      }
      this.content.heading = 'Heading ' + this.id.section + ' ' + this.id.sub_section + ' ' + this.id.slug
      if (this.type === 'blox') {
        this.$set(this, 'blogs',
          [
            {
              id: {
                section: this.id.section,
                sub_section: this.id.subSection,
                slug: 'first'
              },
              type: 'blog',
              content: {
                title: '',
                heading: ''
              }
            }
          ]
        )
      }
    },
    fetchContent: function () {
      if (this.app.app_debug_console) {
        console.log(`fetchContent $route path ${this.$route.path}`)
      }
      this.type = this.$route.path.split('/')[1]
      const isBlogIndex = this.app.site_configuration.types[this.type].is_blog_index
      this.id.section = this.$route.params.section
      this.id.sub_section = this.$route.params.sub_section || ''
      this.id.slug = this.$route.params.slug || ''
      if (this.app.app_debug_console) {
        console.log(`fetchContent str_id ${this.str_id} type ${this.type} isBlogIndex ${isBlogIndex}`)
      }
      if (this.app.app_debug_simul_rest) {
        this.simulFetchContent()
      } else {
        this.$axios.get(`http://dxpydk:8888/${this.type}/${this.str_id}/`)
          .then((response) => {
            this.$set(this, 'meta', response.data.meta)
            this.$set(this, 'content', response.data.content)
            document.title = this.content.title
            this.content_updated = true
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
