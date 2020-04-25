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


class HelloWorldHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world (v2)")


class SiteConfigHandler(tornado.web.RequestHandler):
    def get(self):
        file_name = "data/test_site1/config/site1.yml"
        with open(file_name) as ysd:
            site_config = yaml.load(ysd, Loader=yaml.FullLoader)["config"]
            self.write(json.dumps(site_config, indent=2))


class AppServerMainBase:
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa

    def _arg_parser(self):
        raise NotImplementedError("_arg_parser")

    def __init__(self, name):
        self.name = name
        self.arg_parser = self._arg_parser()
        self.args = None
        self.config = None

    def _do_run(self):
        raise NotImplementedError("_do_run")

    def _do_load_config(self):
        raise NotImplementedError("_do_load_config")

    def _load_config(self):
        self.logger.debug("load_config")
        config_dir = os.getenv('CONFIG_DIR', 'code/config')
        config_name = os.getenv('CONFIG_NAME', self.name) + '.yml'
        with open(f"{config_dir}/{config_name}") as ysd:
            self.config = yaml.load(ysd, Loader=yaml.FullLoader)
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


class OtvlWebServer(AppServerMainBase):
    logger = logging.getLogger(__module__ + "." + __qualname__)  # noqa

    @classmethod
    def _make_app(cls):
        return tornado.web.Application([
            (r"/", HelloWorldHandler),
            (r"/site/config/", SiteConfigHandler),
        ])

    def _arg_parser(self):
        parser = argparse.ArgumentParser(description='OtvlWebServer')
        return parser

    def __init__(self, name):
        AppServerMainBase.__init__(self, name)

    def _do_load_config(self):
        self.logger.debug("_do_load_config OtvlWebServer")

    def _do_run(self):
        self.logger.debug("_do_run OtvlWebServer")
        app = self._make_app()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()
        return True


setup_env()

if __name__ == "__main__":
    cmd_name = os.path.basename(sys.argv[0]).split('.')[0]
    res = OtvlWebServer(cmd_name).run()
    sys.exit(0 if res else -1)
