<template>
  <div id="q-app">
    <router-view v-bind:app="this" />
  </div>
</template>

<script>
import AppUtilMixin from 'src/mixins/AppUtilMixin'
import StandardPage from 'pages/StandardPage'
import BlogIndexPage from 'pages/BlogIndexPage'
import BlogPage from 'pages/BlogPage'

export default {
  mixins: [AppUtilMixin],
  name: 'App',
  data: function () {
    return {
      app_debug: false,
      app_debug_console: true,
      app_debug_simul_rest: false,
      odbg: {},
      pageClassesByName: {
        StandardPage: StandardPage,
        BlogIndexPage: BlogIndexPage,
        BlogPage: BlogPage
      },
      site_configuration: {},
      site_configuration_updated: false,
      site_pages: [],
      site_pages_updated: false,
      brand: {
        toolbar: {
          label: 'toolbar_label_tbd'
        }
      },
      menus: function () {
        return []
      },
      pages_by_id: function () {
        return {}
      }
    }
  },
  created: function () {
    if (this.app_debug_console) {
      console.log('App was created v38')
    }
    this.fetchSiteConfiguration()
  },
  watch: {
    site_configuration_updated () {
      if (this.app_debug_console) {
        console.log('App site_configuration_updated')
      }
      for (const type in this.site_configuration.types) {
        const typeConf = this.site_configuration.types[type]
        typeConf.mapping = this.pageClassesByName[typeConf.mapping]
      }
      this.buildRoutes()
      this.$set(this, 'brand', this.site_configuration.brand)
      if (this.app_debug_console) {
        console.log(`App brand ${this.brand}`)
        console.log(this.brand)
      }
      this.fetchSitePages()
    },
    site_pages_updated () {
      if (this.app_debug_console) {
        console.log('App site_pages_updated')
      }
      this.menus = this.buildMenusFromConf()
      this.pages_by_id = this.buildPagesById()
      // this.$set(this.odbg, 'menus', this.menus)
      this.$set(this.odbg, 'pages_by_id', this.pages_by_id)
    }
  },
  methods: {
    simulFetchSiteConfiguration: function () {
      this.site_configuration = {
        home_section: 'home',
        home_type: 'page',
        types: {
          page: {
            mapping: 'StandardPage',
            has_slug: false
          },
          blox: {
            mapping: 'BlogIndexPage',
            has_slug: false
          },
          blog: {
            mapping: 'BlogPage',
            has_slug: true
          }
        },
        brand: {
          toolbar: {
            label: 'Otvl Web'
          }
        }
      }
    },
    fetchSiteConfiguration: function () {
      if (this.app_debug_simul_rest) {
        this.simulFetchSiteConfiguration()
        this.site_configuration_updated = true
      } else {
        this.$axios.get('http://dxpydk:8888/site/config/')
          .then((response) => {
            this.site_configuration = response.data
            this.site_configuration_updated = true
          })
      }
    },
    buildRoutes: function () {
      this.$router.addRoutes(this.buildRoutesFromConf())
      // this.$set(this.odbg, 'routes', this.buildRoutesFromConf())
    },
    simulFetchSitePages: function () {
      this.site_pages = [
        {
          id: 'home',
          type: 'page',
          menu: 'Home'
        },
        {
          id: 'qi-gong',
          type: 'page',
          menu: 'QI Gong',
          children: [
            {
              id: 'notions-mtc-utiles',
              type: 'page',
              menu: 'Notions de MTC utiles'
            },
            {
              id: 'poumon',
              type: 'page',
              menu: 'Le poumon'
            }
          ]
        },
        {
          id: 'pratique',
          type: 'page',
          menu: 'Pratique',
          children: [
            {
              id: 'association-qi-gong-go',
              type: 'page',
              menu: 'Association Qi Gong Go!'
            },
            {
              id: 'actualites',
              type: 'blox',
              menu: 'Actualités',
              blog_type: 'blog'
            }
          ]
        },
        {
          id: 'blid',
          type: 'blox',
          menu: 'Blog',
          blog_type: 'blog'
        },
        {
          id: 'a-propos',
          menu: 'A propos',
          children: [
            {
              id: 'contact',
              type: 'page',
              menu: 'Nous contacter'
            },
            {
              id: 'association-qi-gong-go',
              type: 'page',
              menu: 'Association Qi Gong Go!'
            },
            {
              id: 'association-chemins-harmonie',
              type: 'page',
              menu: 'Association Les chemins de l\'harmonie'
            },
            {
              id: 'mentions-legales',
              type: 'page',
              menu: 'Mentions légales'
            },
            {
              id: 'confidentialite',
              type: 'page',
              menu: 'Confidentialité'
            }
          ]
        },
        {
          id: 'no-type-no-menu-test',
          menu: 'No type no menu',
          children: [
            {
              id: 'no-sub-menu-here',
              type: 'page'
            }
          ]
        },
        {
          id: 'no-menu-here-test',
          menu: 'No menu here',
          children: [
            {
              id: 'no-sub-menu-there',
              type: 'page'
            },
            {
              id: 'sub-menu-there',
              type: 'page',
              menu: 'A sub menu there'
            }
          ]
        }
      ]
    },
    fetchSitePages: function () {
      if (this.app_debug_simul_rest) {
        this.simulFetchSitePages()
        this.site_pages_updated = true
      } else {
        this.$axios.get('http://dxpydk:8888/site/pages/')
          .then((response) => {
            this.site_pages = response.data
            this.site_pages_updated = true
          })
      }
    }
  }
}
</script>
