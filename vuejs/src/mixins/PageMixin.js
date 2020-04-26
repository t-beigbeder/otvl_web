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
      content: {
        title: '',
        heading: ''
      }
    }
  },
  props: ['app'],
  created: function () {
    this.fetchContent(this.$route.params.section, this.$route.params.sub_section, this.$route.params.slug)
  },
  watch: {
    $route (to, from) {
      this.fetchContent(to.params.section, to.params.sub_section, to.params.slug)
    }
  },
  computed: {
    str_id: function () {
      return this.id.section + '/' + this.id.sub_section + '/' + this.id.slug
    }
  },
  methods: {
    doFetchContent: function (section, subSection, slug) {
      this.id.section = section
      this.id.sub_section = subSection || ''
      this.id.slug = slug || ''
      // TODO: remove this test
      this.content.title = 'Title ' + this.id.section + ' ' + this.id.sub_section + ' ' + this.id.slug
      if (this.content.title) {
        document.title = this.content.title
      }
      this.content.heading = 'Heading ' + this.id.section + ' ' + this.id.sub_section + ' ' + this.id.slug
    },
    fetchContent: function (section, subSection, slug) {
      this.doFetchContent(section, subSection, slug)
    }
  }
}
