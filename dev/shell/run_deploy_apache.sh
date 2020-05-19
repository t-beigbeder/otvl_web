#!/usr/bin/env bash
cmd_dir=`dirname $0`
if [ "`echo $cmd_dir | cut -c1`" != "/" ] ; then
    cmd_dir="`pwd`/$cmd_dir"
fi
base_dir=`echo $cmd_dir | sed -e s=/dev/shell==`
cd $base_dir/vuejs
# quasar build -d
for site in site2 ; do
  rm -rf /srv/www/${site}/web
  mkdir -p /srv/www/${site}/web/assets
  # cp -a dist/spa/. /srv/www/${site}/web
  VERSION="1.0.dev001"
  EXPORT_DIR=/srv/export_dir/guest
  (cd /srv/www/${site}/web && tar xzf ${EXPORT_DIR}/otvl_web_vuejs-${VERSION}.tgz)
  sed -e 's=default_api_server_url=https://site2.dxpydk/api=' -i /srv/www/${site}/web/index.html
  sed -e 's=default_web_server_url=https://site2.dxpydk=' -i /srv/www/${site}/web/index.html
  cp -a ../server/data/test_${site}/assets/. /srv/www/${site}/web/assets/
  chmod -R go+rX /srv/www/${site}
done
