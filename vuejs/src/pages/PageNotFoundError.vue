<template>
  <div class="fixed-center text-center">
    <p>
      <img
        src="statics/img/sad.svg"
        style="width:30vw;max-width:150px;"
      >
    </p>
    <p class="text-faded">
      Sorry, nothing here...<strong>(page not found)</strong>
    </p>
    <q-btn
      style="width:200px;"
      to="/"
      label="Go back"
    />
  </div>
</template>

<script>
export default {
  name: 'PageNotFoundError'
}
</script>
