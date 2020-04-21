# otvl web developper documentation

[documentation index](../README.md)

## Repository structure

This repository is organized as following:

- dev: files used for development
- doc: documentation
- server: a REST API server implemented in python
- vuejs: the web site GUI is implemented with Vue.js and more specifically quasar

## Environment setup

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

Quasar (or try yarn)

    # npm install -g @quasar/cli

### System setup for python

To be completed.

## References

- [node installation](https://github.com/nodesource/distributions/blob/master/README.md#deb)
- [Vue.js](https://vuejs.org/)
- [Quasar framework](https://quasar.dev/)

