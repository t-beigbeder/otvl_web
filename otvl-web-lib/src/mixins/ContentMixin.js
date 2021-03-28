export default {

  props: {
    position: {
      type: Number,
      required: true
    },

    meta: {
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
  },

  mounted() {
    this.$utils.fineDbgLog({'ContentMixin mounted': this, type: this.type})
    this.$state.streamFieldsMounted[this.position] = true
    if ( !this.$utils.configuration.localRouteAnchorClicks || this.type !== "html" ) {
      return;
    }
    const aels = this.$el.getElementsByTagName("a")
    for (let ael of aels) {
      if (!this.isInternalLink(ael)) {
        continue
      }
      this.$utils.fineDbgLog({'ContentMixin content internal link': ael.href, content: this.dbgTextContent()})
      ael.addEventListener('click', event => {
        this.aClickEventHandler(event)
      })
    }
  },

  beforeUnmount(){
    this.$utils.fineDbgLog({'ContentMixin unmounted': this, type: this.type})
    if ( !this.$utils.configuration.localRouteAnchorClicks || this.type !== "html" ) {
      return;
    }
    const aels = this.$el.getElementsByTagName("a")
    for (let ael of aels) {
      if (!this.isInternalLink(ael)) {
        continue
      }
      this.$utils.fineDbgLog({'unmount content internal link': ael.href, content: this.dbgTextContent()})
      ael.removeEventListener('click', event => {
        this.aClickEventHandler(event)
      })
    }
  },

  methods: {
    isInternalLink(ael) {
      // TODO: /assets/ shouldn't be hardcoded
      return !ael.attributes.href.value.startsWith('http') && !ael.attributes.href.value.startsWith('/assets/') && ael.attributes.href.value !== ''
    },

    dbgTextContent() {
      const tc = this.$el.textContent
      if (! tc) {
        return ''
      }
      return tc.substring(0, Math.min(48, tc.length))
    },

    aClickEventHandler(e) {
      this.$utils.fineDbgLog({aClickEventHandler: e})
      // see https://github.com/vuejs/vue-router-next guardEvent()
      // don't redirect with control keys
      if (e.metaKey || e.altKey || e.ctrlKey || e.shiftKey) return
      // don't redirect when preventDefault called
      if (e.defaultPrevented) return
      // don't redirect on right click
      if (e.button !== undefined && e.button !== 0) return
      // don't redirect if `target="_blank"`
      if (e.currentTarget && e.currentTarget.getAttribute) {
        const target = e.currentTarget.getAttribute('target')
        if (/\b_blank\b/i.test(target)) return
      }
      // this may be a Weex event which doesn't have this method
      if (e.preventDefault) e.preventDefault()

      this.$utils.fineDbgLog({aClickEventHandler: 'return true', 'this': this})
      this.$router.push(e.target.attributes.href.value)
      return true
    }
  }

}
