import AppUtilMixin from 'src/mixins/AppUtilMixin'

export default {
  mixins: [AppUtilMixin],
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
        html: ''
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
      this.id.section = this.$route.params.section
      this.id.sub_section = this.$route.params.sub_section || ''
      this.id.slug = this.$route.params.slug || ''
      if (this.app.app_debug_console) {
        console.log(`fetchContent str_id ${this.str_id} type ${this.type}`)
      }
      if (this.app.app_debug_simul_rest) {
        this.simulFetchContent()
      } else {
        this.$axios.get(`http://dxpydk:8888/${this.type}/${this.str_id}/`)
          .then((response) => {
            this.$set(this, 'meta', response.data.meta)
            this.$set(this, 'content', response.data.content)
            document.title = this.content.title
          })
      }
    }
  }
}
