<template>

      <div class="page-content p-2 w-full">
        <div class="py-2 max-w-5xl mx-auto">
          <h2>THIS PAGE WAS NOT FOUND</h2>
        </div>

      </div>

</template>

<script>
import { PageMixin } from 'otvl-web-lib'

export default {
  mixins: [PageMixin],

  name: 'Err404',

  data: function () {
    return {
      'localTitle': 'Page not found'
    }
  }
}
</script>
