# otvl web

This is a web application mainly intended to publish content efficiently.

There is (yet) no GUI, so the content publisher has to update the site
using technical tools to modifiy and upload files.
However, the files structure and their contents remains easy to understand.

- From a content publisher point of view:
  - the site structure and how it is navigable by the end-user through menus/sub-menus
    is configurable;
  - the web application also features a simple blog publish application;
  - the pages content is described by a sequence of textual, graphical or video items, as well
    as hyperlinks and some page layout directive;
  - the site configuration, the pages content,
    media files such as documents, images and video files
    are managed directly as files on the server.

- From a developper point of view:
  - the front-end is developped with
  [Vue.js](https://vuejs.org/)
  and more specifically
  [quasar](https://quasar.dev/)
  layouts and components,
  so the site general _look-and-feel_ may be customized and enriched efficiently;
  - on the server side, a collection of simple REST web services is developped in python,
    their roles mainly being to serve files to the Vue.js client, either directly or
    with trivial yaml-to-json conversion;
  - this simple design also enables to add specific site features through rapid development.

The documentation is organized as following:

- [user documentation](doc/user.md)
- [developper documentation](doc/developper.md)
