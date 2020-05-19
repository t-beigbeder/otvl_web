FROM node:13 as build_stage_1

RUN yarn global add @vue/cli
RUN yarn global add @quasar/cli

RUN mkdir -p /code /shell && chown node:node /code /shell
USER node:node
ADD package.json /tmp/package.json
RUN cd /tmp && yarn

COPY . /code/
WORKDIR /code
RUN ln -s /tmp/node_modules
RUN quasar build
COPY .dev/* /shell/

ENTRYPOINT [ "/shell/docker_entrypoint.sh" ]
CMD [ "/shell/docker_cmd.sh" ]
