FROM httpd:2.4
COPY shell/* /shell/
COPY apache2/conf/ /usr/local/apache2/conf/

ENV WEB_PORT 9981
ENV WEB_SERVER otvl-web-vuejs
ENV API_PORT 9991
ENV API_SERVER otvl-web-server
ENV RPX_PORT 443
ENV RPX_SERVER otvl-web-revproxy

ENV SERVER_NAME vjs-dev-host
ENV APP_PORT 9443

RUN /shell/patch_conf_file_from_env.sh /usr/local/apache2/conf/extra/httpd-ssl.conf
