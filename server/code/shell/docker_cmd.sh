#!/usr/bin/env bash
. /srv/pkg/otvl_web_server_venv/bin/activate
cd ${SRV_DATA} && \
  python \
    -m otvl_web.server \
    -c ${SRV_DATA}/server_config.yml \
    -p ${API_PORT} \
    -a ${API_ADDRESS}