FROM python:3.8-slim as build-stage
RUN apt-get update && apt-get install -y virtualenv && rm -rf /var/lib/apt/lists/*
RUN python -m venv /srv/pkg/otvl_web_server_venv
RUN mkdir -p /code
ADD tools/requirements.txt /code
RUN /srv/pkg/otvl_web_server_venv/bin/pip install -r /code/requirements.txt
ADD code/python /code
WORKDIR /code
RUN /srv/pkg/otvl_web_server_venv/bin/python setup.py install

FROM python:3.8-slim
ARG V_USER=dguest
ARG V_UID=1001
ARG V_GROUP=dguest
ARG V_GID=1001
COPY --from=build-stage /srv/pkg/otvl_web_server_venv /srv/pkg/otvl_web_server_venv
RUN addgroup --gid ${V_GID} ${V_GROUP} && \
  adduser --disabled-password --ingroup ${V_GROUP} --uid ${V_UID} --shell /bin/sh --gecos ${V_USER} ${V_USER}
USER ${V_USER}:${V_GROUP}
ENV OTVL_WEB_CONFIG_PATH=/data/config.yml
ENV OTVL_WEB_HOST=0.0.0.0
ENV OTVL_WEB_INSECURE_CORS=
ENV OTVL_WEB_FULL_ACCESS_LOG=
ENV OTVL_WEB_LOGGING=INFO
ENV OTVL_WEB_PORT=9090
ENV OTVL_WEB_ROOT_PATH=/api/v2

CMD /srv/pkg/otvl_web_server_venv/bin/python -m otvl_web.main
