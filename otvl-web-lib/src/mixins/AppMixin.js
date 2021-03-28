export default {

  methods: {
    fetchConfiguration: function () {
      this.$axios.get(`${this.$utils.configuration.apiServerUrl}/config`)
        .then((response) => {
          this.$state.serverSide = response.data.vuejs
        })
        .catch((error) => {
          this.$utils.dbgLog({'fetchConfiguration': 'error', error})
          this.$router.push('/Err5xx')
        })
    }
  }
}
