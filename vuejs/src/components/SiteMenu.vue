<template>
  <q-btn v-if="has_sub_menus" no-caps unelevated :label="label" icon-right="fas fa-angle-down" :align="align_value" class="BRAND__site-menu-btn" :class="class_value">
    <q-menu>
      <q-list style="min-width: 100px">
        <SiteSubMenu v-for="sub_menu in sub_menus" :key="sub_menu.label" :label="sub_menu.label" :target_url="sub_menu.target_url">
        </SiteSubMenu>
      </q-list>
    </q-menu>
  </q-btn>
  <q-btn v-else no-caps unelevated :label="label" :to="target_url" :align="align_value" class="BRAND__site-menu-btn" :class="class_value">
  </q-btn>
</template>

<script>
import SiteSubMenu from 'src/components/SiteSubMenu'

export default {
  name: 'SiteMenu',

  components: {
    SiteSubMenu
  },

  props: {
    label: {
      type: String,
      required: true
    },

    target_url: {
      type: String,
      required: true
    },

    is_left: {
      type: Boolean,
      default: false
    },

    sub_menus: {
      type: Array,
      default: function () {
        return []
      }
    }
  },
  computed: {
    class_value: function () {
      return '' + (this.is_left ? 'col-12' : '')
    },
    align_value: function () {
      return '' + (this.is_left ? 'left' : '')
    },
    has_sub_menus () {
      return this.sub_menus.length !== 0
    }
  }
}
</script>
