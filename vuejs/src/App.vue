<template>
  <div id="q-app">
    <router-view v-bind:app="this" />
  </div>
</template>

<script>
import { confFromStaticsHttp } from 'src/statics/js/conf.js'

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
      app_debug_console: false,
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
        urls: {
          home: 'urls_home_tbd'
        },
        labels: {
          toolbar: 'toolbar_label_tbd',
          account_tooltip: 'account_tooltip_tbd'
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
    confFromStaticsHttp()
    var qApp = document.getElementById('q-app')
    this.rtc = {
      default_api_server_url: qApp.getAttribute('default-api-server-url'),
      default_web_server_url: qApp.getAttribute('default-web-server-url'),
      api_server_url: qApp.getAttribute('api-server-url'),
      web_server_url: qApp.getAttribute('web-server-url')
    }
    if (this.rtc.web_server_url === 'default_web_server_url') {
      this.rtc.web_server_url = this.rtc.default_web_server_url
    }
    if (this.rtc.api_server_url === 'default_api_server_url') {
      this.rtc.api_server_url = this.rtc.default_api_server_url
    }
    if (this.app_debug_console) {
      console.log('App was created, it102 qApp and rtc')
      console.log(qApp)
      console.log(this.rtc)
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
            has_slug: false,
            is_blog_index: false
          },
          blox: {
            mapping: 'BlogIndexPage',
            has_slug: false,
            is_blog_index: true
          },
          blog: {
            mapping: 'BlogPage',
            has_slug: true,
            is_blog_index: false
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
        this.$axios.get(this.rtc.api_server_url + '/site/config/')
          .then((response) => {
            this.$set(this, 'site_configuration', response.data)
            this.site_configuration_updated = true
          })
          .catch(() => {
            location.replace(`${this.rtc.web_server_url}/statics/error/technical_error.html`)
          })
      }
    },
    buildRoutes: function () {
      this.$router.addRoutes(this.buildRoutesFromConf())
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
        this.$axios.get(this.rtc.api_server_url + '/site/pages/')
          .then((response) => {
            this.site_pages = response.data
            this.site_pages_updated = true
          })
          .catch(() => {
            this.$router.push('/err')
          })
      }
    }
  }
}
</script>
