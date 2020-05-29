<template>
  <div>
    <div v-if="is_header &&  !('brand' in page.content && 'no_dates' in page.content.brand && page.content.brand.no_dates)">
      <div v-if="page.meta_headers.creation_date" class="text-caption">
        {{ app.brand.labels.created_on }} {{ page.intlDate(page.meta_headers.creation_date, app.brand.locale) }}
      </div>
      <div v-if="page.meta_headers.publication_date" class="text-caption">
        {{ app.brand.labels.published_on }} {{ page.intlDate(page.meta_headers.publication_date, app.brand.locale) }}
      </div>
      <div v-if="page.meta_headers.last_update_date" class="text-caption">
        {{ app.brand.labels.last_updated_on }} {{ page.intlDate(page.meta_headers.last_update_date, app.brand.locale) }}
      </div>
    </div>
    <div v-if="!is_header &&  !('brand' in page.content && 'no_dates' in page.content.brand && page.content.brand.no_dates)">
      <div v-if="page.meta_footers.creation_date" class="text-caption">
        {{ app.brand.labels.created_on }} {{ page.intlDate(page.meta_footers.creation_date, app.brand.locale) }}
      </div>
      <div v-if="page.meta_footers.publication_date" class="text-caption">
        {{ app.brand.labels.published_on }} {{ page.intlDate(page.meta_footers.publication_date, app.brand.locale) }}
      </div>
      <div v-if="page.meta_footers.last_update_date" class="text-caption">
        {{ app.brand.labels.last_updated_on }} {{ page.intlDate(page.meta_footers.last_update_date, app.brand.locale) }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageHeaderAndFooter',

  props: {
    is_header: {
      type: Boolean
    },
    app: {
      type: Object,
      required: true
    },
    page: {
      type: Object,
      required: true
    }
  }
}
</script>
