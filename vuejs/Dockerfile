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
