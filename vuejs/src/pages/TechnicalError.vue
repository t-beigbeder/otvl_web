<template>
  <div class="fixed-center text-center">
    <p>
      <img
        src="statics/img/sad.svg"
        style="width:30vw;max-width:150px;"
      >
    </p>
    <p class="text-faded">
      Sorry, a technical problem prevents to display this page...
    </p>
    <p class="text-faded">
      Please try again later, or...
    </p>
    <q-btn
      color="secondary"
      style="width:200px;"
      to="/"
      label="Go back"
    />
  </div>
</template>

<script>
export default {
  name: 'TechnicalError'
}
</script>
