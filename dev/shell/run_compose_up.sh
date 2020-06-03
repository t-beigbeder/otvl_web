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

export VAR_DATA_TMP=${base_dir}/dev/tmp
if [ -z "$1" ] ; then
  data_origin="${base_dir}/server/docker_data"
else
  data_origin="$1"
fi

true && \
  echo rm -rf ${VAR_DATA_TMP}/* && \
  info "Exporting site data from ${data_origin} in ${VAR_DATA_TMP}" && \
  cp -r ${data_origin}/. ${VAR_DATA_TMP}/ && \
  run_command docker-compose -f ${base_dir}/dev/compose/docker-compose.yml up -d && \
  true || exit 1
info "By default, the demo site is available at https://vjs-dev-host:9443"
info "Stop the stack with ${base_dir}/dev/shell/run_compose_down.sh"
exit 0