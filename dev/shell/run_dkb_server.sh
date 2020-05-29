#!/usr/bin/env bash

cmd_dir=`dirname $0`
if [ "`echo $cmd_dir | cut -c1`" != "/" ] ; then
    cmd_dir="`pwd`/$cmd_dir"
fi
base_dir=`echo $cmd_dir | sed -e s=/dev/shell==`
cd $base_dir
if [ -f ${base_dir}/dev/shell/common_dev.sh ] ; then
    . ${base_dir}/dev/shell/common_dev.sh
else
    echo >&2 "No ${base_dir}/dev/shell/common_dev.sh"
    exit 1
fi
VERSION="1.0.dev008"
EXPORT_DIR=/srv/export_dir/guest
run_command docker build --pull \
  --build-arg V_USER=`id -un` \
  --build-arg V_UID=`id -u` \
  --build-arg V_GROUP=`id -gn` \
  --build-arg V_GID=`id -g` \
  -t otvl_web_server:${VERSION} server && \
  info "run command docker run --rm otvl_web_server:${VERSION}" && \
  docker run --rm otvl_web_server:${VERSION} > ${EXPORT_DIR}/otvl_web_server_venv-${VERSION}.tgz && \
  run_command ls -l ${EXPORT_DIR}/otvl_web_server_venv-${VERSION}.tgz && \
  info "Archive ${EXPORT_DIR}/otvl_web_server_venv-${VERSION}.tgz is available" && \
  true || exit 1
