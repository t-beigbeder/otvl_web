<template>
  <q-card bordered class="my-card">
    <q-card-section>
      <div class="text-h6">{{ title }}</div>
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
    title: {
      type: String,
      required: true
    }
  }
}
</script>
