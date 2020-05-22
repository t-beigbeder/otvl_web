FROM python:3.7-slim-stretch as build_stage_1
RUN apt-get update && LC_ALL=C DEBIAN_FRONTEND=noninteractive apt-get install -yqq --no-install-recommends \
        virtualenv \
&& rm -rf /var/lib/apt/lists/*
RUN /usr/bin/virtualenv -p /usr/local/bin/python /srv/venv/otvl_web
RUN mkdir -p /code
ADD requirements.txt /code
RUN /srv/venv/otvl_web/bin/pip install -r /code/requirements.txt

FROM python:3.7-slim-stretch as build_stage_2
COPY --from=build_stage_1 /srv/venv/otvl_web /srv/venv/otvl_web
ADD code/python /code
WORKDIR /code
RUN /srv/venv/otvl_web/bin/python setup.py install

FROM python:3.7-slim-stretch
ARG V_USER=dguest
ARG V_UID=1001
ARG V_GROUP=dguest
ARG V_GID=1001

COPY --from=build_stage_2 /srv/venv/otvl_web /srv/venv/otvl_web
RUN addgroup --gid ${V_GID} ${V_GROUP} && \
  adduser --disabled-password --ingroup ${V_GROUP} --uid ${V_UID} --shell /bin/sh --gecos ${V_USER} ${V_USER}
COPY code/shell/* /shell/
USER ${V_USER}:${V_GROUP}

ENTRYPOINT [ "/shell/docker_entrypoint.sh" ]
CMD [ "/shell/docker_cmd.sh" ]
