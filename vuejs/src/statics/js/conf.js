var confFromStaticsHttp = function () {
  var qApp = document.getElementById('q-app')
  qApp.setAttribute('default-api-server-url', 'http://vjs-dev-host:8888/api')
  qApp.setAttribute('default-web-server-url', 'http://vjs-dev-host:8080')
}
export { confFromStaticsHttp }
