var confFromStaticsHttp = function () {
  var qApp = document.getElementById('q-app')
  qApp.setAttribute('default-api-server-url', 'http://dxpydk:8888/api')
  qApp.setAttribute('default-web-server-url', 'http://dxpydk:8080/#')
}
export { confFromStaticsHttp }
