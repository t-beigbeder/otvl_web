FROM node:18-slim as build-stage

COPY otvl-web-lib/ /otvl_web/otvl-web-lib/
WORKDIR /otvl_web/otvl-web-lib
RUN yarn global add @vue/cli @vue/cli-service \
  && yarn install \
  && yarn build-lib

COPY otvl-web-sample/public /otvl_web/otvl-web-sample/public
COPY otvl-web-sample/src /otvl_web/otvl-web-sample/src
COPY otvl-web-sample/*.js* /otvl_web/otvl-web-sample/
WORKDIR /otvl_web/otvl-web-sample
RUN yarn install \
  && yarn build

FROM httpd:2.4
COPY --from=build-stage /otvl_web/otvl-web-sample/dist /srv/www/site1/web
COPY otvl-web-sample/shell /shell
COPY otvl-web-sample/apache2/conf /usr/local/apache2/conf
COPY otvl-web-sample/apache2/web /srv/www/site1/web
ENV OTVL_WEB_SERVER_NAME demo.otvl.org
ENV OTVL_WEB_APP_PORT 443
CMD /shell/httpd-foreground.sh
