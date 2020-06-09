<template>
  <div>
    <q-separator spaced class="col-12 q-mt-sm-xl" size="1px" color="blue-grey-2"/>
    <div class="row fit column items-center">
      <q-card flat>
        <span v-for="(menu, ix) in app.menus[app.brand.bottom_menu.index].sub_menus" :key="menu.label">
          {{ menu.label }}
          <span v-if="ix == 0">.</span>
        </span>
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
