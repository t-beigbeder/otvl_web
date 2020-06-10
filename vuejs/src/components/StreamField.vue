<template>
  <span v-if="type == 'html'" v-html="content"></span>
  <div v-else-if="type == 'sf_q_img_in_card'" class="row">
    <q-card class="col-auto q-mb-md">
      <img :src="src" :alt=alt :title=title :class=class_>
    </q-card>
    <p v-if="credit"><i><a :href=credit.href>{{ credit.text }}</a></i></p>
  </div>
  <div v-else-if="type == 'sf_page_dates'">
    <div v-if="meta.creation_date" class="text-caption">
      {{ brand.labels.created_on }} {{ intlDate(meta.creation_date, brand.locale) }}
    </div>
    <div v-if="meta.publication_date" class="text-caption">
      {{ brand.labels.published_on }} {{ intlDate(meta.publication_date, brand.locale) }}
    </div>
    <div v-if="meta.last_update_date" class="text-caption">
      {{ brand.labels.last_updated_on }} {{ intlDate(meta.last_update_date, brand.locale) }}
    </div>
    <div class="text-caption">&nbsp;</div>
  </div>
  <span v-else>type unknown: {{ type }}</span>
</template>

<script>
import { DateTime } from 'luxon'

export default {
  name: 'StreamField',
  props: {
    meta: {
      type: Object,
      required: true
    },

    brand: {
      type: Object,
      required: true
    },

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
    },
    alt: {
      type: String,
      required: false
    },
    title: {
      type: String,
      required: false
    },
    class_: {
      type: String,
      required: false
    },
    credit: {
      type: String,
      required: false
    }
  },
  methods: {
    intlDate: function (isoDateStr, locale) {
      const dt = DateTime.fromISO(isoDateStr)
      const res = dt.setLocale(locale).toLocaleString(DateTime.DATE_MED)
      return res
    }
  }
}
</script>
