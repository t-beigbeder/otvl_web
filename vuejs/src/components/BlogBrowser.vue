<template>
  <q-card bordered class="my-card">
    <q-card-section>
      <q-item tag="a" :to="index_url" class="text-h6" style="text-decoration: none">
        {{ index_title }}
      </q-item>
    </q-card-section>

    <q-separator inset />

    <q-card-section>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua.
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: 'BlogBrowser',

  props: {
    index_title: {
      type: String,
      required: true
    },
    index_url: {
      type: String,
      required: true
    }
  }
}
</script>
