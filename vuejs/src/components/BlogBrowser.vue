<template>
  <q-card>
    <q-card-section class="q-py-none">
      <div class="q-my-sm text-h6 text-blue-grey-8 text-center">
        {{ brand.labels.search_blogs }}
      </div>
    </q-card-section>

    <q-separator inset />

    <q-card-section class="q-py-none">
      <q-item dense tag="a" :to="index_url" class="q-my-sm text-blue-grey-8" style="text-decoration: none">
        {{ brand.labels.index_title }}
      </q-item>
      <q-item dense disable tag="a" :to="index_url" class="q-my-sm text-blue-grey-8" style="text-decoration: none">
        {{ brand.labels.search_criteria }}
      </q-item>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: 'BlogBrowser',

  props: {
    app: {
      type: Object,
      required: true
    },
    brand: {
      type: Object,
      required: true
    },
    index_url: {
      type: String,
      required: true
    }
  }
}
</script>
