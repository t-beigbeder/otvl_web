<template>
  <div v-if="app.bottom_menu" class="page-bottom">
    <q-separator spaced class="col-12 q-mt-sm-xl" size="1px" color="blue-grey-2"/>
    <div class="row fit column items-center">
      <q-card flat>
        <span v-for="(menu, ix) in app.bottom_menu" :key="menu.label">
          <router-link :to="menu.target_url">{{ menu.label }}</router-link>
          <span v-if="ix != app.bottom_menu.length - 1">
            <b>&middot;</b>
          </span>
        </span>
        <q-separator spaced class="col-12" size="1px" color="blue-grey-2"/>
      </q-card>
    </div>
  </div>
</template>

<script>

export default {
  name: 'PageBottom',

  props: {
    app: {
      type: Object,
      required: true
    }
  }
}
</script>
