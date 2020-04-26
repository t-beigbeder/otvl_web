import SiteLayout from 'src/layouts/SiteLayout'
import Error404 from 'src/pages/Error404'

export default {
  methods: {
    getApp: function () {
      return ('app' in this) ? this.app : this
    },
    buildRoutesFromConf: function () {
      const app = this.getApp()
      const routes = []
      for (const type in app.site_configuration.types) {
        const typeConf = app.site_configuration.types[type]
        const slugSuffix = typeConf.has_slug ? '/:slug' : ''
        routes.push(
          {
            path: `/${type}/:section/:sub_section${slugSuffix}`,
            component: SiteLayout,
            children: [
              {
                path: '/',
                component: typeConf.mapping
              }
            ]
          }
        )
        routes.push(
          {
            path: `/${type}/:section${slugSuffix}`,
            component: SiteLayout,
            children: [
              {
                path: '/',
                component: typeConf.mapping
              }
            ]
          }
        )
      }
      routes.push(
        {
          path: '/',
          redirect: `/${app.site_configuration.home_type}/${app.site_configuration.home_section}`
        }
      )
      routes.push(
        {
          path: '*',
          component: Error404
        }
      )
      return routes
    },
    has_sub_menu: function (page) {
      if (!('children' in page)) {
        return false
      }
      for (const child of page.children) {
        if ('menu' in child) {
          return true
        }
      }
      return false
    },
    build_url: function (page, parent) {
      if (!parent) {
        return `/${page.type}/${page.id}`
      }
      return `/${page.type}/${parent.id}/${page.id}`
    },
    buildMenusFromConf: function () {
      const app = this.getApp()
      const menus = []
      for (var index = 0; index < app.site_pages.length; index++) {
        const page = app.site_pages[index]
        if ((!('type' in page) || !('menu' in page)) && !this.has_sub_menu(page)) {
          continue
        }
        if (!this.has_sub_menu(page)) {
          menus.push(
            {
              label: page.menu,
              target_url: this.build_url(page)
            }
          )
          continue
        }
        const menu = {
          label: page.menu,
          target_url: this.build_url(page),
          sub_menus: []
        }
        if ('type' in page) {
          menu.sub_menus.push(
            {
              label: page.menu,
              target_url: this.build_url(page)
            }
          )
        }
        for (var index2 = 0; index2 < page.children.length; index2++) {
          const child = page.children[index2]
          if (!('menu' in child)) {
            continue
          }
          menu.sub_menus.push(
            {
              label: child.menu,
              target_url: this.build_url(child, page)
            }
          )
        }
        menus.push(menu)
      }
      return menus
    },
    buildPagesById: function () {
      const app = this.getApp()
      const pagesById = {}
      for (var index = 0; index < app.site_pages.length; index++) {
        const page = app.site_pages[index]
        const pageId = `${page.id}//`
        if ('type' in page) {
          pagesById[pageId] = page
        }
        if (!('children' in page)) {
          continue
        }
        for (var index2 = 0; index2 < page.children.length; index2++) {
          const child = page.children[index2]
          if (!('type' in child)) {
            continue
          }
          const childId = `${page.id}/${child.id}/`
          pagesById[childId] = child
        }
      }
      return pagesById
    },
    getPageById: function (pageId) {
      const app = this.getApp()
      return app.pages_by_id[pageId]
    }
  }
}
