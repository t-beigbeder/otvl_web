#!/usr/bin/env sh

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