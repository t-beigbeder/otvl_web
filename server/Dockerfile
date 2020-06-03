FROM debian:buster-slim as build_stage_1
RUN apt-get update && LC_ALL=C DEBIAN_FRONTEND=noninteractive apt-get install -yqq --no-install-recommends \
        python3 \
        virtualenv \
        libexpat1 \
&& rm -rf /var/lib/apt/lists/*
RUN /usr/bin/virtualenv -p python3 /srv/pkg/otvl_web_server_venv
RUN mkdir -p /code
ADD requirements.txt /code
RUN /srv/pkg/otvl_web_server_venv/bin/pip install -r /code/requirements.txt
ADD code/python /code
WORKDIR /code
RUN /srv/pkg/otvl_web_server_venv/bin/python setup.py install

FROM debian:buster-slim
ARG V_USER=dguest
ARG V_UID=1001
ARG V_GROUP=dguest
ARG V_GID=1001
RUN apt-get update && LC_ALL=C DEBIAN_FRONTEND=noninteractive apt-get install -yqq --no-install-recommends \
        python3 \
        libexpat1 \
&& rm -rf /var/lib/apt/lists/*

COPY --from=build_stage_1 /srv/pkg/otvl_web_server_venv /srv/pkg/otvl_web_server_venv
RUN addgroup --gid ${V_GID} ${V_GROUP} && \
  adduser --disabled-password --ingroup ${V_GROUP} --uid ${V_UID} --shell /bin/sh --gecos ${V_USER} ${V_USER}
COPY code/shell/* /shell/
COPY docker_data/config/ /srv/data/config/
COPY docker_data/pages/ /srv/data/pages/
USER ${V_USER}:${V_GROUP}

ENV SRV_DATA /srv/data
ENV API_PORT 9991
ENV API_ADDRESS otvl-web-server

CMD [ "/shell/docker_cmd.sh" ]
