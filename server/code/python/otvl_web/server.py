import logging
import os
import traceback
import argparse
import sys
import json

import tornado.ioloop
import tornado.web
import yaml


def setup_env():
    logging.basicConfig(
        level=os.getenv('LOGGING', 'INFO'),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class BaseHandler(tornado.web.RequestHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa
    server_config = {}

    def initialize(self, **kwargs):
        BaseHandler.server_config = kwargs["server_config"]
        del kwargs["server_config"]
        super().initialize(**kwargs)

    def prepare(self):
        self.logger.debug(f"prepare: {self.request.method} {self.request.path}")
        self.set_header("Content-Type", "application/json")
        if "Origin" in self.request.headers and \
                "cors_mapping" in self.server_config and \
                self.request.headers["Origin"] in self.server_config["cors_mapping"]:
            origin_allowed = self.request.headers["Origin"]
            self.logger.debug(f"prepare CORS authorized for {origin_allowed}")
            self.set_header("Access-Control-Allow-Origin", origin_allowed)

    def _check_par(self, name, par):
        if not par:
            self._error(400, 'MissingParameter', 'Parameter {0} is missing in URL'.format(name))
            return par
        return True

    def _error(self, code, reason, message):
        self.clear()
        self.set_status(code)
        self.finish({'reason': reason, 'message': message})


class VersionHandler(BaseHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa

    def initialize(self, **kwargs):
        super().initialize(**kwargs)

    def get(self):
        config_file = self.server_config["site_config_file"]
        self.logger.debug(f"GET: site_config_file {config_file}")
        self.write(json.dumps(self.server_config["version"], indent=2))
        return self.finish()


class SiteHandler(BaseHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa

    def initialize(self, **kwargs):
        super().initialize(**kwargs)

    def get(self):
        config_file = self.server_config["site_config_file"]
        self.logger.debug(f"GET: site_config_file {config_file}")
        key = self.request.path[len("/site/"):]
        if key[-1] == "/":
            key = key[:-1]
        with open(config_file) as ysd:
            site_config = yaml.load(ysd, Loader=yaml.FullLoader)[key]
            self.write(json.dumps(site_config, indent=2))
            return self.finish()


class PageHandler(BaseHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa

    def initialize(self, **kwargs):
        super().initialize(**kwargs)

    def _get_page_content(self, section, sub_section, slug):
        file_path = self.server_config["pages_directory"]
        if file_path[-1] != "/":
            file_path += "/"
        file_path += section
        if sub_section:
            file_path += "/"
            file_path += sub_section
        if slug:
            file_path += "/"
            file_path += slug
        try:
            with open(file_path + ".emd", encoding="utf-8") as fd:
                return fd.read()
        except FileNotFoundError:
            return None

    def get(self, type_, section, *path_args):
        config_file = self.server_config["site_config_file"]
        sub_section, slug = '', ''
        if len(path_args) > 0:
            sub_section = path_args[0]
            if len(path_args) > 1:
                slug = path_args[1]
        self.logger.debug(f"GET: site_config_file {config_file} type '{type_}' section '{section}' sub_section '{sub_section}' slug '{slug}'")  # noqa
        if not self._check_par("section", section):
            return
        page_content = self._get_page_content(section, sub_section, slug)
        if not page_content:
            return self._error(404, 'ResourceNotFound', 'The page content is missing')
        self.write(json.dumps(dict(page_content=page_content), indent=2))
        return self.finish()


class AppServerMainBase:
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa
    server_config = None

    def _arg_parser(self):
        raise NotImplementedError("_arg_parser")

    def __init__(self, name):
        self.name = name
        self.arg_parser = self._arg_parser()
        self.args = None
        self.config_file = None

    def _do_run(self):
        raise NotImplementedError("_do_run")

    def pre_load_config(self):
        pass

    def _do_load_config(self):
        raise NotImplementedError("_do_load_config")

    def _load_config(self):
        self.logger.debug("load_config")
        self.pre_load_config()
        if self.config_file is None:
            config_dir = os.getenv('CONFIG_DIR', 'code/config')
            config_name = os.getenv('CONFIG_NAME', self.name) + '.yml'
            self.config_file = f"{config_dir}/{config_name}"
        with open(self.config_file) as ysd:
            self.__class__.server_config = yaml.load(ysd, Loader=yaml.FullLoader)
        self._do_load_config()

    def run(self):
        self.args = self.arg_parser.parse_args()
        try:
            self._load_config()
            self.logger.info('run: start')
            result = self._do_run()
            self.logger.info('run: done')
            return result
        except Exception as e:
            traceback.print_exc()
            self.logger.error(
                'An unkonwn error occured, please contact the support - {0} {1}'.format(
                    type(e), e))
        self.logger.info('run: done')
        return False


def make_otvl_web_app(server_config):
    handler_kwa = {
        "server_config": server_config
        }
    return tornado.web.Application([
        (r"/version/?", VersionHandler, handler_kwa),
        (r"/site/config/?", SiteHandler, handler_kwa),
        (r"/site/pages/?", SiteHandler, handler_kwa),
        (r"/([^/]*)/([^/]*)/([^/]*)/([^/]*)/?", PageHandler, handler_kwa),
        (r"/([^/]*)/([^/]*)/([^/]*)/?", PageHandler, handler_kwa),
        (r"/([^/]*)/([^/]*)/?", PageHandler, handler_kwa),
    ])


class OtvlWebServer(AppServerMainBase):
    logger = logging.getLogger(__module__ + "." + __qualname__)  # noqa

    @classmethod
    def _make_app(cls):
        return make_otvl_web_app(cls.server_config)

    def _arg_parser(self):
        parser = argparse.ArgumentParser(description='OtvlWebServer')
        parser.add_argument('-c', '--config', type=str, help='Configuration file')
        parser.add_argument('-p', '--port', type=int, help='port to bind the server (defaults to OW_PORT env var or 8888)')  # noqa
        parser.add_argument('-a', '--address', type=str, help='host or IP address to listen to, empty string implies all interfaces (defaults to OW_ADDRESS or empty)')  # noqa
        return parser

    def __init__(self, name):
        AppServerMainBase.__init__(self, name)

    def pre_load_config(self):
        self.logger.debug("pre_load_config OtvlWebServer")
        self.config_file = self.args.config

    def _do_load_config(self):
        self.logger.debug("_do_load_config OtvlWebServer")

    def _do_run(self):
        self.logger.debug("_do_run OtvlWebServer")
        if self.args.port:
            port = self.args.port
        else:
            port = int(os.getenv("OW_PORT", "8888"))
        if self.args.address:
            address = self.args.address
        else:
            address = os.getenv("OW_ADDRESS", "")
        app = self._make_app()
        app.listen(port, address)
        tornado.ioloop.IOLoop.current().start()
        return True


setup_env()

if __name__ == "__main__":
    cmd_name = os.path.basename(sys.argv[0]).split('.')[0]
    res = OtvlWebServer(cmd_name).run()
    sys.exit(0 if res else -1)
