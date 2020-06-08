<template>
  <span v-if="type == 'html'" v-html="content"></span>
  <q-card v-else-if="type == 'sf_q_img_in_card'">
    <img :src="src">
  </q-card>
  <span v-else>type unknown: {{ type }}</span>
</template>

<script>
export default {
  name: 'StreamField',
  props: {
    type: {
      type: String,
      required: true
    },

    content: {
      type: String,
      required: false
    },

    src: {
      type: String,
      required: false
    }
  }
}
</script>
