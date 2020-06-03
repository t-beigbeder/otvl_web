#!/usr/bin/env sh

DK_ACT_VERSION="1.0.act001"
export VAR_ACT_S_IMAGE="otvl_web_server:${DK_ACT_VERSION}"
export VAR_ACT_V_IMAGE="otvl_web_vuejs:${DK_ACT_VERSION}"
export VAR_ACT_R_IMAGE="otvl_web_revproxy:${DK_ACT_VERSION}"

log() {
  TS=`date +%Y/%m/%d" "%H:%M:%S",000"`
  echo "$TS | $1 | script: $2"
}

error() {
  log ERROR "$1"
}

warn() {
  log WARNING "$1"
}

info() {
  log INFO "$1"
}

run_command() {
    info "run command \"$*\""
    "$@" || (error "while running command \"$*\"" && return 1)
}