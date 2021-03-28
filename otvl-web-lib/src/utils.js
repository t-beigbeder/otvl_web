const utils = {

  configuration: {
    debug: false,
    fineDebug: false,
    localRouteAnchorClicks: false
  },

  dbgLog: function (msg) {
    if (this.configuration.debug) {
      console.log(msg)
    }
  },

  fineDbgLog: function (msg) {
    if (this.configuration.fineDebug) {
      console.log(msg)
    }
  }

}

export default utils
