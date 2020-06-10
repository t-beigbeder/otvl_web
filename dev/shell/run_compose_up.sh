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
  data_origin1="${base_dir}/server/docker_data"
  data_origin2="${base_dir}/vuejs/.dev/docker/data"
else
  data_origin1="$1"
  data_origin2="$1"
fi

true && \
  rm -rf ${VAR_DATA_TMP}/* && \
  info "Exporting site data from ${data_origin} in ${VAR_DATA_TMP}" && \
  cp -r ${data_origin1}/. ${VAR_DATA_TMP}/ && \
  cp -r ${data_origin2}/. ${VAR_DATA_TMP}/ && \
  run_command docker-compose -f ${base_dir}/dev/compose/docker-compose.yml up -d && \
  true || exit 1
info "By default, the demo site is available at https://vjs-dev-host:9443"
info "Stop the stack with ${base_dir}/dev/shell/run_compose_down.sh"
exit 0