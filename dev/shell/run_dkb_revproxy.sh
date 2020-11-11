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
if [ -z "${DKB_R_VERSION}" ] ; then
  VERSION="1.0.dev002"
else
  VERSION="${DKB_R_VERSION}"
fi
EXPORT_DIR=/srv/export_dir/guest
run_command \
  docker build --pull \
    -t otvl_web_revproxy:${VERSION} revproxy && \
  true || exit 1
