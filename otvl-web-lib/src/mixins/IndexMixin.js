export default {

  data: function () {
    return {
      isIndex: true
    }
  },

  created() {
    this.$watch(
      () => this.$route.path,
      () => {
        this.$utils.fineDbgLog({
          'watch in IndexMixin': 'route.path',
          'route.path': this.$route.path,
          'isIndex': this.$route.meta.isIndex
        })

        if ( this.$route.meta.isIndex
          && (this.$route.path !== this.$state.loadedXPath)
          && (this.$route.path !== this.$state.xpathLoading) ) {
          this.fetchIndex()
        }
      },
      // fetch the data when the view is created and the data is
      // already being observed
      { immediate: true }
    )
  },

  methods: {
    fetchIndex() {
      var pathLoading = this.$route.path
      this.$state.xpathLoading = this.$route.path
      this.$utils.dbgLog({'fetchIndex': 'xpathLoading', 'route': this.$route})

      this.$axios.get(`${this.$utils.configuration.apiServerUrl}/index${this.$route.path}`)
        .then((response) => {

          if (pathLoading === this.$state.xpathLoading) {
            this.$state.xpathLoading = null
            this.$state.loadedXPath = pathLoading
            this.$state.loadedIndex = response.data
            this.$utils.dbgLog({'fetchIndex': 'loadedXPath', 'loadedIndex': this.$state.loadedIndex})
          }
        })
        .catch((error) => {

          if (pathLoading === this.$state.xpathLoading) {
            this.$state.xpathLoading = null
            this.$state.loadedXPath = null
            this.$state.loadedIndex = null

            if (error.response && error.response.status == 404) {
              this.$utils.dbgLog({'fetchIndex': 'error404', error})
              this.$router.replace('/Err404')
            }
            else {
              this.$utils.dbgLog({'fetchIndex': 'error5xx', error})
              this.$router.replace('/Err5xx')
            }
          }
        })
    },

    index() {
      return this.$state.loadedIndex ? this.$state.loadedIndex.index : []
    }
  }
}
