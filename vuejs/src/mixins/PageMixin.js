import AppUtilMixin from 'src/mixins/AppUtilMixin'
import StreamField from 'src/components/StreamField'
import PageBottom from 'src/components/PageBottom'
import { DateTime } from 'luxon'

export default {
  mixins: [AppUtilMixin],

  components: {
    StreamField,
    PageBottom
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
        brand: {
          no_dates: false
        },
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
    },
    meta_headers: function () {
      const res = {
      }
      if (this.app.brand.behavior.dates_header) {
        res.creation_date = this.meta.creation_date
        res.publication_date = this.meta.publication_date
        res.last_update_date = this.meta.last_update_date
      }
      return res
    },
    meta_footers: function () {
      const res = {
      }
      if (this.app.brand.behavior.dates_footer) {
        res.creation_date = this.meta.creation_date
        res.publication_date = this.meta.publication_date
        res.last_update_date = this.meta.last_update_date
      }
      return res
    }
  },
  methods: {
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
