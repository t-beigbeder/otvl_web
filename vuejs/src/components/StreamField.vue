<template>
  <span v-if="type == 'html'" v-html="content"></span>
  <div v-else-if="type == 'sf_q_img_in_card'" class="row" :class="row_class">
    <q-card class="column col-auto q-mb-md">
      <img :src="src" :alt=alt :title=title :class=class_>
    </q-card>
    <p v-if="credit"><i><a :href=credit.href>{{ credit.text }}</a></i></p>
  </div>
  <div v-else-if="type == 'sf_q_cards'" class="row">
    <div v-for="(card, index) in elements" :key="index" class="col-grow col-md-3 col-sm-4 q-mx-sm">
      <q-card>
        <q-card-section class="bg-blue-grey-1 q-ma-none q-pa-sm">
          <div class="text-h6 text-blue-grey-8 text-center">
            {{ card.title }}
          </div>
        </q-card-section>
        <q-card-section class="q-my-sm">
          <span v-html="card.content"></span>
        </q-card-section>
      </q-card>
    </div>
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
    },
    elements: {
      type: Array,
      required: false
    },
    row_class: {
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
