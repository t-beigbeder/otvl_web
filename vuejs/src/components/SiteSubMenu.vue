<template>
  <q-item clickable v-close-popup :to="target_url" dense  active-class="BRAND__site-menu-item" class="BRAND__site-menu-item q-ml-md">
    {{ label }}
  </q-item>
</template>

<script>
export default {
  name: 'SiteSubMenu',
  props: {
    label: {
      type: String,
      required: true
    },

    target_url: {
      type: String,
      required: true
    }
  }
}
</script>
