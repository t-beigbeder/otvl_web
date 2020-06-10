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

# run_dkb_for_compose [ "r" | "s" | "v" | "rs" | "rv" | "sv" ]
v_r=1
v_s=1
v_v=1
if [ -n "$1" ] ; then
  v_r=`echo "$1" | grep "r"`
  v_s=`echo "$1" | grep "s"`
  v_v=`echo "$1" | grep "v"`
fi
export DKB_R_VERSION="${DK_ACT_VERSION}"
export DKB_S_VERSION="${DK_ACT_VERSION}"
export DKB_V_VERSION="${DK_ACT_VERSION}"
export DKB_NO_EXPORT=1

true && \
  ([ -z "$v_r" ] || ${base_dir}/dev/shell/run_dkb_revproxy.sh) && \
  ([ -z "$v_s" ] || ${base_dir}/dev/shell/run_dkb_server.sh) && \
  ([ -z "$v_v" ] || ${base_dir}/dev/shell/run_dkb_vuejs.sh) && \
  true || exit 1
