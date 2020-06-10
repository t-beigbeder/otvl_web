FROM node:13 as build_stage_1

RUN yarn global add @vue/cli
RUN yarn global add @quasar/cli

RUN mkdir -p /code /shell && chown node:node /code /shell
USER node:node
ADD package.json /tmp/package.json
RUN cd /tmp && yarn

COPY . /code/
WORKDIR /code
RUN ln -s /tmp/node_modules
RUN quasar build

FROM httpd:2.4
COPY --from=build_stage_1 /code/dist/spa/ /srv/www/site1/web/
COPY .dev/docker/shell/* /shell/
COPY .dev/docker/apache2/conf/ /usr/local/apache2/conf/
COPY .dev/docker/data/assets/ /srv/data/assets/
RUN ln -s /srv/data/assets /srv/www/site1/web/

ENV WEB_PORT 9981
ENV WEB_SERVER otvl-web-vuejs

ENV API_PORT 9991
ENV SERVER_NAME vjs-dev-host
ENV APP_PORT 9443

RUN /shell/patch_conf_file_from_env.sh /usr/local/apache2/conf/httpd.conf
RUN /shell/patch_conf_file_from_env.sh /srv/www/site1/web/index.html
