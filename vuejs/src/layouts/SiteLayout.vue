<template>
  <q-layout view="lHh Lpr fff" class="bg-grey-1">
    <q-header elevated class="bg-white text-grey-8" height-hint="64">
      <div class="fit row wrap justify-start items-start content-start">
        <q-toolbar class="col-auto BRAND__toolbar" style="height: 64px">
          <q-btn
            v-if="$q.screen.lt.md"
            flat
            dense
            round
            @click="leftDrawerOpen = !leftDrawerOpen"
            aria-label="Menu"
            icon="menu"
            class="q-mx-md"
          />
          <q-item tag="a" to="/page/home">
              <img src="~assets/brand_logo.jpg">
          </q-item>
          <q-toolbar-title>
            <q-item tag="a" to="/page/home" class="text-grey-8" style="text-decoration: none">
              {{ app.brand.toolbar.label }}
            </q-item>
          </q-toolbar-title>
        </q-toolbar>

        <q-toolbar v-if="$q.screen.gt.sm" class="col-grow BRAND__toolbar" style="height: 64px">
          <SiteMenu v-for="menu in app.menus" v-bind="menu" :key="menu.id">
          </SiteMenu>
        </q-toolbar>
        <q-toolbar v-if="$q.screen.lt.md" class="col-grow BRAND__toolbar" style="height: 64px">
        </q-toolbar>
        <q-toolbar class="col-1 BRAND__toolbar" style="height: 64px">
          <q-btn flat round dense disable>
            <q-avatar size="26px">
              <img src="~assets/user.png">
            </q-avatar>
            <q-tooltip>Account</q-tooltip>
          </q-btn>
        </q-toolbar>
      </div>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      bordered
      behavior="mobile"
      @click="leftDrawerOpen = false"
    >
      <q-scroll-area class="fit">
        <q-toolbar class="BRAND__toolbar">
          <q-toolbar-title class="row items-center text-grey-8">
            <img class="q-pl-md" src="~assets/brand_logo.jpg">
            <span class="q-ml-sm">Ateliers du QI</span>
          </q-toolbar-title>
        </q-toolbar>

        <q-list class="row">
          <SiteMenu v-for="menu in app.menus" v-bind="menu" :key="menu.id" :is_left="true">
          </SiteMenu>
        </q-list>
      </q-scroll-area>
    </q-drawer>
    <q-page-container class="BRAND__page-container">
      <p v-if="app.app_debug">SiteLayout odbg {{ app.odbg }}</p>
      <router-view v-bind:app="app"/>
    </q-page-container>
  </q-layout>
</template>

<script>
import SiteMenu from 'components/SiteMenu'

export default {
  name: 'SiteLayout',

  components: {
    SiteMenu
  },

  data () {
    return {
      leftDrawerOpen: false
    }
  },
  props: ['app']
}
</script>

<style lang="sass">
.BRAND

  &__toolbar
    height: 64px

  &__toolbar-input
    width: 35%

  &__drawer-item
    line-height: 24px
    border-radius: 0 24px 24px 0
    margin-right: 12px

    .q-item__section--avatar
      padding-left: 12px
      .q-icon
        color: #5f6368

    .q-item__label:not(.q-item__label--caption)
      color: #3c4043
      letter-spacing: .01785714em
      font-size: .875rem
      font-weight: 500
      line-height: 1.25rem

    &--storage
      border-radius: 0
      margin-right: 0
      padding-top: 24px
      padding-bottom: 24px

  &__site-menu-btn
    color: $grey-8
    &__label
      font-size: 12px
      line-height: 24px
      letter-spacing: .01785714em
      font-weight: 500

  &__site-menu-item
    color: $grey-8

  @media (min-width: 1024px)
    &__page-container
      padding-left: 94px

</style>
