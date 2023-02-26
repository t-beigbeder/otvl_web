# otvl web developer documentation

[documentation index](../README.md)

## Repository structure

This repository is organized as following:

- dev: files used for development
- doc: documentation
- revproxy: a reverse proxy apache2 configuration for docker
- server: a REST API server implemented in python
- vuejs: the web site GUI is implemented with Vue.js

## Environment setup

### General system setup

Add otvl-dev-host as alias to development host.

### System setup for Vue.js (debian)

Install [nvm](https://github.com/nvm-sh/nvm#install--update-script)

    $ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash    
    $ nvm install lts/hydrogen
    $ nvm use lts/hydrogen

Testing local distribution

### Vue.js app

    cd otvl-web-lib
    yarn install
    yarn build-lib
    cd ../otvl-web-sample
    yarn install
    yarn build
    yarn serve

### System setup for python

    # in a virtualenv
    pip install pip-tools
    pip-compile tools/requirements.in
    pip-compile tools/requirements-dev.in
    pip-sync tools/requirements.txt tools/requirements-dev.txt

## Testing locally without docker

### Python part

Run the API server with the following environment (sample):

    OTVL_WEB_CONFIG_PATH=data/tests/unit_test_server02/config.yml
    OTVL_WEB_HOST=0.0.0.0
    OTVL_WEB_INSECURE_CORS=1
    OTVL_WEB_LOGGING=DEBUG
    OTVL_WEB_PORT=9090
    OTVL_WEB_RELOAD=1
    OTVL_WEB_ROOT_PATH=/api/v2

### Vue.js part

Build the library:

    # in otvl-web-lib
    yarn install
    yarn build-lib

Install the library in the demo application:

    # in otvl-web-sample or clone
    yarn install
    # or when library otvl-web-lib is updated
    yarn add ../../otvl_web/otvl-web-lib

Run the vue.js application development server

    # in otvl-web-sample or clone
    yarn serve

Configure the vue.js application in `otvl-web-sample/src/app/apputils.js`

Setup a vue.js (v3) application from scratch

    # create a vue.js application with vue cli
    vue create otvl-web-sample
    # add dependencies (sample)
    yarn add axios luxon vue-router@4 \
      tailwindcss@npm:@tailwindcss/postcss7-compat postcss@^7 autoprefixer@^9 \
      ../../otvl_web/otvl-web-lib
    # for tailwindcss configure tailwind.config.js and postcss.config.js as intended

## Testing locally with docker-compose

    # run a stack with traefik reverse proxy, apache web server and FastAPI API server
    docker-compose -f docker-compose-local.yml up -d --build
    # check log files
    docker-compose -f docker-compose-local.yml logs -f
    # update development
    # update the stack
    docker-compose -f docker-compose-local.yml up -d --build
    # clean up
    docker-compose -f docker-compose-local.yml down
    docker system prune

The application will be accessible at [https://otvl-dev-host:9443/](https://otvl-dev-host:9443/)

## References

- [node installation](https://github.com/nodesource/distributions/blob/master/README.md#deb)
- [Vue.js v3](https://v3.vuejs.org/)
- [Vue Router v4](https://next.router.vuejs.org/)
