<template>
  <q-layout>
    <h4>{{ content.heading }}</h4>
    <p>This is a blog index page.</p>
    <p>The section is {{ $route.params.section }}</p>
    <p>The sub_section is {{ $route.params.sub_section }}</p>
    <p>The slug is {{ $route.params.slug }}</p>
    <p>The str_id is {{ str_id }}</p>

    <p v-if="app.app_debug">site_configuration {{ app.site_configuration }}</p>

    <ul id="blogs">
      <li v-for="item in blogs" :key="item.str_id">
        <router-link :to="blogPrefixLink + '/' + item.id.slug">{{ item.id.slug }}</router-link>
      </li>
    </ul>
    <q-page-container>
      <router-view></router-view>
    </q-page-container>
  </q-layout>
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
    fetchContent: function (section, subSection) {
      this.doFetchContent(section, subSection)
      // TODO: remove this test
      this.$set(this, 'blogs',
        [
          {
            id: {
              section: section,
              sub_section: subSection,
              slug: 'first'
            },
            content: {
              title: '',
              heading: ''
            }
          }
        ]
      )
    }
  }
}
</script>
