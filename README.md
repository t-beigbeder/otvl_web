# otvl_web

Otvl_web is an
[Open Source](https://en.wikipedia.org/wiki/Free_and_open-source_software)
web application whose main objective is to publish digital content efficiently.

It is built with the
[Vue.js framework](https://vuejs.org/)
as a
_[single-page application](https://en.wikipedia.org/wiki/Single-page_application)_.

There is at this time no GUI for editing a site content,
so the content publisher has to update the site
using technical tools to modifiy and upload files.
However, the files structure, their contents and their organization remain easy to understand.

You will find useful references at the bottom of this page.

The documentation is organized as following:

- general presentation: this one
- [user documentation](doc/user.md) not yet written
- [developer documentation](doc/developer.md)

## General presentation

### For content publishers

From a content publisher point of view, the benefits of this tool are that

- the site structure and how it is navigable by the end-user through menus/sub-menus
  is easily configurable;
- the web application also features a simple application for blog publishing;
- the site configuration, the pages content, media files such as documents, images and video files
  are managed directly as files on the server;
- the site configuration and the pages metadata are described through
  [YAML](https://yaml.org/)
  files, a simple language to describe structured data;
- the pages contents are described in
  [markdown](https://daringfireball.net/projects/markdown/syntax),
  a simple language widely used to describe web page contents;
- the underlying
  _[single-page application](https://en.wikipedia.org/wiki/Single-page_application)_
  architecture enables smoother pages transitions and uses less data over the network;
- the underlying technology can provide the user with
  a high level of ergonomy:
  you may browse the collection of
  [Quasar Vue Components](https://quasar.dev/vue-components/)
  for instance, to make your opinion;
- the simple publication application can be extended to provide dedicated features
  through rapid development.

Uploading YAML and markdown source files along with media files
is an efficient way of working in organizations where the site publisher
and the site administrator are the same person.

As mentioned above, there is no GUI for editing content.
The content publisher must have direct or indirect access to the content files on the server.
An example of indirect access is the use of [git](https://git-scm.com/) along with triggers
to upload files after commit.

There is yet no access control on the published content either.

### For developers

From a developer point of view, the benefits of this tool are that

- the front-end is developped with
  [Vue.js](https://vuejs.org/)
  so the site general _look-and-feel_ may be customized and enriched efficiently;
- on the server side, a collection of simple REST web services are developped in python,
  their roles being mainly to serve files to the Vue.js client, either directly or
  with trivial yaml-to-json conversion;
- this simple design also enables to add specific site features through rapid development.

### For operations

Concerning the deployment of the otvl_web application,
single-page applications require specific configuration
on the server-side to handle the URL otherwise routed on the client-side,
but also to support web crawler robots.

Some questions and solutions specific to the deployment of a Vue.js
_single-page application_ are detailed in the article
_[Deploying a Vue.js Single Page Application](https://blog.otvl.org/blog/otvl-blog/deploy-vjs-spa)_:

- the application supports web crawler bots through sitemap.xml generation
  and server-side HTML rendering;
- a static Vue.js site may be configured at deployment time concerning the actual DNS name
  of the reverse proxy.

The following topics are detailed in the
[developer documentation](doc/developer.md):

- produce docker images
- simulate deployment with docker compose
- ansible playbooks

### Current status

This application
is still a work-in-progress,
however it is already hosting a few web sites in production.

The first concern at this time is obviously the lack of documentation.
However this gap may be filled easily, thus quickly,
moreover, several samples that are used for tests
and a demonstration site can help to start a new site.

## Useful links

### Articles and guides

- [codemag - HTML5 History](https://www.codemag.com/Article/1301091/HTML5-History-Clean-URLs-for-Deep-linking-Ajax-Applications)
- [css-tricks - Using the HTML5 History API](https://css-tricks.com/using-the-html5-history-api/)
- [mozilla - Working with the History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API/Working_with_the_History_API)
- [vue router - HTML5 History Mode](https://router.vuejs.org/guide/essentials/history-mode.html)
- [otvl blog - Deploying a Vue.js Single Page Application](/blog/otvl-blog/deploy-vjs-spa)

### References

- [Vue.js](https://vuejs.org/)
- [Quasar framework](https://quasar.dev/)
- [History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API)
- [otvl_web project](https://github.com/t-beigbeder/otvl_web)
