import { nextTick } from 'vue'

export default {

  created() {
    this.$watch(
      () => this.$route.path,
      () => {
        this.$utils.fineDbgLog({
          'watch in PageMixin': 'route.path',
          'route.path': this.$route.path,
          'route': this.$route,
          'isIndex': this.$route.meta.isIndex
        })

        if ( (this.$route.path !== this.$state.loadedPath)
          && (this.$route.path !== this.$state.pathLoading) ) {
          if (! this.$route.meta.isLocal) {
            this.fetchContent()
          }
          else if (this.$route.meta.isLocal) {
            this.$state.pathLoading = null
            this.$state.loadedPath = null
          }
        }

      },
      // fetch the data when the view is created and the data is
      // already being observed
      { immediate: true }
    )
  },

  mounted() {
    this.$utils.fineDbgLog({'PageMixin mounted': this, streamFieldsMounted: this.streamFieldsMounted})
    if (this.$route.meta.isLocal) {
      document.title = this.localTitle ? this.localTitle : this.$route.path
    }
  },

  beforeUnmount(){
    this.$utils.fineDbgLog({'PageMixin unmounted': this})
  },

  computed: {

    state() {
      return this.$state
    },

    content() {
      return this.$state.loadedContent ? this.$state.loadedContent.content : {}
    },

    meta() {
      return this.$state.loadedContent ? this.$state.loadedContent.meta : {}
    },

    streamFields() {
      return (!this.$state.pathLoading && this.$state.loadedContent) ? this.$state.loadedContent.content.stream_fields : []
    },

    streamFieldsMounted() {
      let res = this.$state.streamFieldsMounted.every((sfm) => sfm)
      this.$utils.fineDbgLog({'streamFieldsMounted': res, 'length': this.$state.streamFieldsMounted.length})
      return res
    }

  },

  watch: {
    content() {
      document.title = this.content.title
    },

    streamFields() {
      this.$utils.fineDbgLog({'streamFields changed': this, streamFieldsMounted: this.streamFieldsMounted})
      if ( this.$state.streamFieldsMounted.length === 0 ) {
        return
      }
      if ( this.streamFieldsMounted ) {
        this.scrollToSaved()
        return
      }

      nextTick(() => {
        this.$utils.fineDbgLog({'streamFields changed nextTick': this, streamFieldsMounted: this.streamFieldsMounted})
        if ( this.$state.streamFieldsMounted.length !== 0 && this.streamFieldsMounted ) {
          this.scrollToSaved()
          return
        }
      })

    }
  },

  methods: {
    fetchContent() {
      var pathLoading = this.$route.path
      this.$state.pathLoading = this.$route.path
      this.$state.loadedContent = null
      this.$state.streamFieldsMounted = []
      this.$utils.dbgLog({'fetchContent': 'pathLoading', 'route': this.$route})

      this.$axios.get(`${this.$utils.configuration.apiServerUrl}/content${this.$route.path}`)
        .then((response) => {

          if (pathLoading === this.$state.pathLoading) {
            this.$state.pathLoading = null
            this.$state.loadedPath = pathLoading
            if ( response.data.content.stream_fields ) {
              this.$state.streamFieldsMounted = new Array(response.data.content.stream_fields.length).fill(false)
              this.$utils.fineDbgLog({'fetchContent tmp': 'loadedPath', 'state': this.$state, 'streamFieldsMounted': this.streamFieldsMounted})
            }
            this.$state.loadedContent = response.data
            this.$utils.dbgLog({'fetchContent': 'loadedPath', 'state': this.$state, 'streamFieldsMounted': this.$state.streamFieldsMounted})
          }
        })
        .catch((error) => {

          if (pathLoading === this.$state.pathLoading) {
            this.$state.pathLoading = null
            this.$state.loadedPath = null
            this.$state.loadedContent = null

            if (error.response && error.response.status == 404) {
              this.$utils.dbgLog({'fetchContent': 'error404', error})
              this.$router.replace('/Err404')
            }
            else {
              this.$utils.dbgLog({'fetchContent': 'error5xx', error})
              this.$router.replace('/Err5xx')
            }
          }
        })
    },

    scrollToSaved() {
      if (this.$state.scrollStatus && this.$state.scrollStatus.savedPosition) {
        this.$utils.fineDbgLog({'scrollToSaved top': this.$state.scrollStatus.savedPosition.top})
        window.scrollTo(0, this.$state.scrollStatus.savedPosition.top)
      }
    }
  }
}
