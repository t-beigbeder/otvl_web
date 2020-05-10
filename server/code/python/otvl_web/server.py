import logging
import os
import traceback
import argparse
import sys
import json
import glob
from operator import itemgetter

import tornado.ioloop
import tornado.web
import yaml
import markdown


def setup_env():
    logging.basicConfig(
        level=os.getenv('LOGGING', 'INFO'),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class BaseHandler(tornado.web.RequestHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa
    server_config = {}
    site_config = {}

    def initialize(self, **kwargs):
        BaseHandler.server_config = kwargs["server_config"]
        del kwargs["server_config"]
        BaseHandler.site_config = kwargs["site_config"]
        del kwargs["site_config"]
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


class BasePageHandler(BaseHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa
    md = None

    def initialize(self, **kwargs):
        super().initialize(**kwargs)

    def _md2html(self, md_text):
        extensions = [
            "attr_list",
            "footnotes",
            "tables",
            "codehilite",
            "toc"
            ]
        if self.md is None:
            BasePageHandler.md = markdown.Markdown(extensions=extensions)
        return self.md.convert(md_text)

    def _load_page_content(self, page_file_path):
        try:
            with open(page_file_path, encoding="utf-8") as ypc_fd:
                page_content = yaml.load(ypc_fd, Loader=yaml.FullLoader)
                return page_content
        except FileNotFoundError:
            self.logger.debug(f"_load_page_content: file_path {page_file_path} FileNotFoundError")
            return None

    def _get_page_content(self, section, sub_section, slug, as_html=True):
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
            file_path += ".yml"
            page_content = self._load_page_content(file_path)
            for sf in page_content["content"]["stream_fields"]:
                if sf["type"] == "md_file":
                    md_file_path = os.path.dirname(file_path) + "/" + sf["file"]
                    with open(md_file_path, encoding="utf-8") as md_fd:
                        sf["type"] = "html"
                        sf["content"] = self._md2html(md_fd.read())
                        del sf["file"]
                elif sf["type"] == "md_data":
                    sf["type"] = "html"
                    sf["content"] = self._md2html(sf["data"])
                    del sf["data"]
            return page_content
        except FileNotFoundError:
            self.logger.debug(f"_get_page_content: file_path {file_path} FileNotFoundError")
            return None


class PageHandler(BasePageHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa

    def initialize(self, **kwargs):
        super().initialize(**kwargs)

    def get(self, type_, section, *path_args):
        config_file = self.server_config["site_config_file"]
        sub_section, slug = '', ''
        if len(path_args) > 0:
            sub_section = path_args[0]
            if len(path_args) > 1:
                slug = path_args[1]
        self.logger.debug(f"GET: site_config_file {config_file} type '{type_}' section '{section}' sub_section '{sub_section}' slug '{slug}'")  # noqa
        if type_ not in self.site_config["config"]["types"]:
            return self._error(400, 'BadParameter', 'Parameter type {0} is unknown'.format(type_))
        if not self._check_par("section", section):
            return
        page_content = self._get_page_content(section, sub_section, slug)
        if not page_content:
            return self._error(404, 'ResourceNotFound', 'The page content is missing')
        self.write(json.dumps(page_content, indent=2))
        return self.finish()


class BlogsHandler(BasePageHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa

    def initialize(self, **kwargs):
        super().initialize(**kwargs)

    def _load_blogs(self, file_path):
        blog_infos = {}
        blob_paths = glob.glob(f"{file_path}/**/*.yml", recursive=True)
        for blog_path in blob_paths:
            blog_name = os.path.basename(blog_path)[0:-len(".yml")]
            blog_infos[blog_name] = {"slug": blog_name}
            blog_content = self._load_page_content(blog_path)
            for meta_field, meta_value in blog_content["meta"].items():
                blog_infos[blog_name][meta_field] = meta_value
        return blog_infos

    def _get_blogs_index(self, section, sub_section):
        file_path = self.server_config["pages_directory"]
        if file_path[-1] != "/":
            file_path += "/"
        file_path += section
        if sub_section:
            file_path += "/"
            file_path += sub_section
        blogs = self._load_blogs(file_path)
        blog_index = []
        for info in blogs.values():
            blog_index.append(info)
        return sorted(blog_index, key=itemgetter("publication_date"), reverse=True)
        return blog_index

    def get(self, section, *path_args):
        config_file = self.server_config["site_config_file"]
        sub_section = ''
        if len(path_args) > 0:
            sub_section = path_args[0]
        self.logger.debug(f"GET: site_config_file {config_file} section '{section}' sub_section '{sub_section}'")  # noqa
        if not self._check_par("section", section):
            return
        blogs = {
            "blogs": self._get_blogs_index(section, sub_section)
            }
        self.write(json.dumps(blogs, indent=2))
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
    site_config_file = server_config["site_config_file"]
    with open(site_config_file) as ysd:
        site_config = yaml.load(ysd, Loader=yaml.FullLoader)

    handler_kwa = {
        "server_config": server_config,
        "site_config": site_config
        }
    assets_directory = server_config["assets_directory"]
    return tornado.web.Application([
        (r"/version/?", VersionHandler, handler_kwa),
        (r"/site/config/?", SiteHandler, handler_kwa),
        (r"/site/pages/?", SiteHandler, handler_kwa),
        (r"/assets/(.*)", tornado.web.StaticFileHandler, {"path": assets_directory}),
        (r"/blogs/([^/]*)/([^/]*)/([^/]*)/?", BlogsHandler, handler_kwa),
        (r"/blogs/([^/]*)/([^/]*)/?", BlogsHandler, handler_kwa),
        (r"/blogs/([^/]*)/?", BlogsHandler, handler_kwa),
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
