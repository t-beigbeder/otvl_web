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

Node and npm

    # curl -sL https://deb.nodesource.com/setup_13.x | bash -
    # apt-get install gcc g++ make
    # apt-get install -y nodejs
    # node -v
    v13.5.0
    # npm -v
    6.13.4

Yarn (recommended)

    # curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
    # echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
    # apt-get update && apt-get install yarn
    # yarn -v
    1.21.1

vue.js

    $ yarn global add @vue/cli
    $ vi ~/.profile
    if [ -d "$HOME/.yarn/bin" ] ; then
        PATH="$HOME/.yarn/bin:$PATH"
    fi
    $ vue --version
    @vue/cli 4.1.2


vue serve

    $ yarn global add @vue/cli-service

Testing local distribution

    $ yarn global add serve
    $ yarn build
    $ serve -s dist

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
