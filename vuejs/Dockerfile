FROM node:13 as build_stage_1

RUN yarn global add @vue/cli
RUN yarn global add @quasar/cli

RUN mkdir -p /code /shell && chown node:node /code /shell
USER node:node
COPY . /code/
WORKDIR /code
RUN yarn install
RUN quasar build
COPY .dev/shell/export_from_docker_vuejs.sh /shell/

ENTRYPOINT [ "/shell/export_from_docker_vuejs.sh" ]
