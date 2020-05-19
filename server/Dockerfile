FROM python:3.7-slim-stretch as build_stage_1
RUN apt-get update && LC_ALL=C DEBIAN_FRONTEND=noninteractive apt-get install -yqq --no-install-recommends \
        virtualenv \
&& rm -rf /var/lib/apt/lists/*
RUN /usr/bin/virtualenv -p /usr/local/bin/python /venv
RUN mkdir -p /code
ADD requirements.txt /code
RUN /venv/bin/pip install -r /code/requirements.txt

FROM python:3.7-slim-stretch as build_stage_2
COPY --from=build_stage_1 /venv /venv
ADD code/python /code
WORKDIR /code
RUN /venv/bin/python setup.py install

FROM python:3.7-slim-stretch
ARG V_USER=dguest
ARG V_UID=1001
ARG V_GROUP=dguest
ARG V_GID=1001

COPY --from=build_stage_2 /venv /venv
RUN addgroup --gid ${V_GID} ${V_GROUP} && \
  adduser --disabled-password --ingroup ${V_GROUP} --uid ${V_UID} --shell /bin/sh --gecos ${V_USER} ${V_USER}
COPY code/shell/export_from_docker_server.sh /shell/
USER ${V_USER}:${V_GROUP}

ENTRYPOINT [ "/shell/export_from_docker_server.sh" ]
