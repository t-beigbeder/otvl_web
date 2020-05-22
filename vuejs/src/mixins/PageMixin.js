import AppUtilMixin from 'src/mixins/AppUtilMixin'
import StreamField from 'src/components/StreamField'
import { DateTime } from 'luxon'

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
      }
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
    $route: function () {
      if (this.app.app_debug_console) {
        console.log(`watch $route: path ${this.$route.path}`)
      }
      this.fetchContent()
    }
  },
  computed: {
    str_id: function () {
      return this.id.section + '/' + this.id.sub_section + '/' + this.id.slug
    },
    locale: function () {
      return this.app.brand.locale
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
      this.id.section = this.$route.params.section
      this.id.sub_section = this.$route.params.sub_section || ''
      this.id.slug = this.$route.params.slug || ''
      if (this.app.app_debug_console) {
        console.log(`fetchContent str_id ${this.str_id} type ${this.type}`)
      }
      if (this.app.app_debug_simul_rest) {
        this.simulFetchContent()
      } else {
        this.$axios.get(`${this.app.rtc.api_server_url}/${this.type}/${this.str_id}/`)
          .then((response) => {
            this.$set(this, 'meta', response.data.meta)
            this.$set(this, 'content', response.data.content)
            document.title = this.content.title
            if (this.app.site_configuration.types[this.type].blog_type) {
              this.fetchBlogIndex()
            }
          })
          .catch((error) => {
            if (error.response && error.response.status === 404) {
              location.replace(`${this.app.rtc.web_server_url}/statics/error/page_not_found.html`)
            } else {
              location.replace(`${this.app.rtc.web_server_url}/statics/error/technical_error.html`)
            }
          })
      }
    },
    intlDate: function (isoDateStr, locale) {
      const dt = DateTime.fromISO(isoDateStr)
      const res = dt.setLocale(locale).toLocaleString(DateTime.DATE_MED)
      if (this.app.app_debug_console) {
        console.log(`intlDate ${isoDateStr} - ${locale} - ${dt} - ${res}`)
      }
      return res
    }
  }
}
