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

true && \
  run_command docker-compose -f ${base_dir}/dev/compose/docker-compose.yml down && \
  true || exit 1
info "Stop the stack with ${base_dir}/dev/shell/run_compose_down.sh"
exit 0