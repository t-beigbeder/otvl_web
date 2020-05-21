<template>
  <q-card bordered>
    <q-card-section class="q-py-none">
      <div class="q-my-sm text-h6 text-grey-8 text-center">
        {{ app.brand.labels.search_blogs }}
      </div>
    </q-card-section>

    <q-separator inset />

    <q-card-section class="q-py-none">
      <q-item dense tag="a" :to="index_url" class="q-my-sm text-grey-8" style="text-decoration: none">
        {{ brand.labels.index_title }}
      </q-item>
      <q-item dense disable tag="a" :to="index_url" class="q-my-sm text-grey-8" style="text-decoration: none">
        {{ brand.labels.blog_index_search_criteria }}
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
