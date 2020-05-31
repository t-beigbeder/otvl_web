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
      routes_configured: false,
      brand: {
        urls: {
          home: 'urls_home_tbd'
        },
        assets: {
        },
        labels: {
          toolbar: 'toolbar_label_tbd',
          account_tooltip: 'account_tooltip_tbd'
        },
        behavior: {
          dates_header: false,
          dates_footer: false
        }
      },
      menus: function () {
        return []
      },
      pages_by_id: function () {
        return {}
      },
      assets_url: 'assets_url_tbd'
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
    if ((this.rtc.web_server_url === 'default_web_server_url') || !this.rtc.web_server_url) {
      this.rtc.web_server_url = this.rtc.default_web_server_url
    }
    if (this.rtc.api_server_url === 'default_api_server_url' || !this.rtc.api_server_url) {
      this.rtc.api_server_url = this.rtc.default_api_server_url
    }
    if (this.app_debug_console) {
      console.log('App was created, it104 qApp and rtc')
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
      this.assets_url = this.site_configuration.assets_url
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
    fetchSiteConfiguration: function () {
      this.$axios.get(this.rtc.api_server_url + '/site/config/')
        .then((response) => {
          this.$set(this, 'site_configuration', response.data)
          this.site_configuration_updated = true
        })
        .catch(() => {
          location.replace(`${this.rtc.web_server_url}/statics/error/technical_error.html`)
        })
    },
    buildRoutes: function () {
      if (!this.routes_configured) {
        this.routes_configured = true
        const routes = this.buildRoutesFromConf()
        if (this.app_debug_console) {
          console.log('buildRoutes')
          console.log(routes)
        }
        this.$router.addRoutes(routes)
      } else {
        if (this.app_debug_console) {
          console.log('buildRoutes: up to date')
        }
      }
    },
    fetchSitePages: function () {
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
</script>
