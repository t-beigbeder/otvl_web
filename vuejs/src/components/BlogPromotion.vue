<template>
  <q-card bordered class="bg-blue-grey-1">
    <q-card-section class="q-py-none">
      <div class="q-my-sm text-h6 text-red-10 text-center">
        {{ brand.labels.promotion }}
      </div>
    </q-card-section>

    <q-separator inset />

    <q-card-section class="q-py-none">
      <q-item
        v-for="blog in preview_blogs"
        :key="blog.slug" dense tag="a"
        :to="blog_prefix_link + '/' + blog.slug"
        class="q-px-none q-my-sm text-caption"
        style="text-decoration: none"
      >
        {{ blog.summary_heading }}
      </q-item>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: 'BlogPromotion',

  props: {
    app: {
      type: Object,
      required: true
    },
    brand: {
      type: Object,
      required: true
    },
    preview_blogs: {
      type: Array,
      required: true
    },
    blog_prefix_link: {
      type: String,
      required: true
    }
  }
}
</script>
