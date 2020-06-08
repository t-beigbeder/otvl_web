import logging
import os
import traceback
import argparse
import sys
import json
import glob
from operator import itemgetter
import datetime

import tornado.ioloop
import tornado.web
import yaml
import markdown

import otvl_web.j24bots


logger = logging.getLogger(__name__)


def setup_env():
    logging.basicConfig(
        level=os.getenv('LOGGING', 'INFO'),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa

    def set_extra_headers(self, path):
        self.logger.debug("set_extra_headers")
        self.set_header("Cache-control", "no-cache")


class BaseHandler(tornado.web.RequestHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa
    server_config = {}
    site_config = {}
    j24bots_loader = None

    def initialize(self, **kwargs):
        BaseHandler.server_config = kwargs["server_config"]
        del kwargs["server_config"]
        BaseHandler.site_config = kwargs["site_config"]
        del kwargs["site_config"]
        BaseHandler.j24bots_loader = kwargs["j24bots_loader"]
        del kwargs["j24bots_loader"]
        super().initialize(**kwargs)

    def prepare(self):
        self.logger.debug(f"prepare: {self.request.method} {self.request.path}")
        if not self.request.path.endswith(".xml"):
            if "/html4/" not in self.request.path:
                self.set_header("Content-Type", "application/json")
            else:
                self.set_header("Content-Type", "text/html")
        else:
            self.set_header("Content-Type", "text/xml; charset=utf-8")
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

    def _load_page_content(self, page_file_path):
        try:
            with open(page_file_path, encoding="utf-8") as ypc_fd:
                page_content = yaml.load(ypc_fd, Loader=yaml.FullLoader)
                return page_content
        except FileNotFoundError:
            self.logger.debug(f"_load_page_content: file_path {page_file_path} FileNotFoundError")
            return None

    def _load_blogs(self, file_path):
        blog_infos = {}
        blog_paths = glob.glob(f"{file_path}/**/*.yml", recursive=True)
        for blog_path in blog_paths:
            blog_name = os.path.basename(blog_path)[0:-len(".yml")]
            blog_content = self._load_page_content(blog_path)
            blog_infos[blog_name] = {
                "slug": blog_name,
                }
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
        key = self.request.path[len("/api/site/"):]
        if key[-1] == "/":
            key = key[:-1]
        config_o = self.site_config[key]
        if key == "config":
            if "assets_url" in self.server_config:
                config_o["assets_url"] = self.server_config["assets_url"]
            else:
                config_o["assets_url"] = config_o["default_assets_url"]

        self.write(json.dumps(config_o, indent=2))
        return self.finish()


class BasePageHandler(BaseHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa
    default_assets_url = None
    assets_url = None

    def initialize(self, **kwargs):
        super().initialize(**kwargs)
        BasePageHandler.default_assets_url = self.site_config["config"]["default_assets_url"]
        if "assets_url" not in self.server_config:
            BasePageHandler.assets_url = self.default_assets_url
        else:
            BasePageHandler.assets_url = self.server_config["assets_url"]

    def _get_url(self):
        if "base_url" in self.server_config:
            loc = f"/{self.server_config['base_url']}"
        else:
            loc = ""
        loc += f"/{self.path_args[0]}/{self.path_args[1]}"
        for ix in (2, 3):
            if len(self.path_args) > ix:
                if self.path_args[ix] != "":
                    loc += f"/{self.path_args[ix]}"
        return loc

    def _patch_html_loc_anchors(self, html_text):
        loc_anchor_str = 'href="#'
        page_url_str = self._get_url()
        while loc_anchor_str in html_text:
            ix = html_text.index(loc_anchor_str)
            html_text = html_text[0:ix + len(loc_anchor_str) - 1] + page_url_str \
                + html_text[ix + len(loc_anchor_str) - 1:]
        return html_text

    def _patch_html_src_assets(self, html_text):
        if self.assets_url == self.default_assets_url:
            return html_text
        src_asset_str = f'src="{self.default_assets_url}'
        server_asset_str = f'src="{self.assets_url}'
        while src_asset_str in html_text:
            ix = html_text.index(src_asset_str)
            html_text = html_text[0:ix] + server_asset_str + html_text[ix + len(src_asset_str):]
        return html_text

    def _patch_asset_in_src_sf(self, src_sf):
        if self.assets_url == self.default_assets_url or self.default_assets_url not in src_sf:
            return src_sf
        ix = src_sf.index(self.default_assets_url)
        src_sf = src_sf[0:ix] + self.assets_url + src_sf[ix + len(self.default_assets_url):]
        return src_sf

    def _patch_assets_wiki_links(self, md_text):
        if self.assets_url == self.default_assets_url:
            return md_text
        src_asset_str = f'[[{self.default_assets_url}'
        server_asset_str = f'[[{self.assets_url}'
        while src_asset_str in md_text:
            ix = md_text.index(src_asset_str)
            md_text = md_text[0:ix] + server_asset_str + md_text[ix + len(src_asset_str):]
        return md_text

    def _md2html(self, md_text):
        extensions = [
            "attr_list",
            "footnotes",
            "tables",
            "codehilite",
            "toc",
            "mdx_wikilink_plus"
            ]
        extension_configs = {}

        if "base_url" in self.server_config:
            extension_configs["mdx_wikilink_plus"] = {"base_url": self.server_config["base_url"]}
        md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
        patched_md_text = self._patch_assets_wiki_links(md_text)
        html_text = md.convert(patched_md_text)
        patched_assets_html_text = self._patch_html_src_assets(html_text)
        patched_anchors_html_text = self._patch_html_loc_anchors(patched_assets_html_text)
        return patched_anchors_html_text

    def _serialize_first_div(self, html_text):
        changed = False
        start = html_text
        div, end = None, None
        div_bx = html_text.find("<div otvl-web>\n")
        if div_bx == -1:
            return changed, start, div, end
        changed = True
        start = html_text[:div_bx]
        end = html_text[div_bx + len("<div otvl-web>\n"):]
        cdiv_bx = end.find("</div>\n")
        if cdiv_bx == -1:
            return changed, start, div, end
        div = end[:cdiv_bx]
        try:
            div = yaml.load(div, Loader=yaml.FullLoader)
        except yaml.parser.ParserError:
            pass
        end = end[cdiv_bx + len("</div>\n"):]
        return changed, start, div, end

    def _serialize_divs_in_content(self, page_content):
        serialized_sf = []
        for sf in page_content["content"]["stream_fields"]:
            if sf["type"] != "html":
                serialized_sf.append(sf)
                continue
            changed = True
            next = sf["content"]
            while changed:
                changed, start, div, end = self._serialize_first_div(next)
                serialized_sf.append(dict(type="html", content=start))
                if changed:
                    if div is not None:
                        if type(div) is str:
                            div = dict(type="html", content=div)
                        serialized_sf.append(div)
                    next = end
        return serialized_sf

    def _get_page_content(self, section, sub_section, slug):
        file_path = self.server_config["pages_directory"]
        if file_path[-1] != "/":
            file_path += "/"
        file_path += section
        if sub_section:
            file_path += "/"
            file_path += sub_section
        if slug:
            blog_paths = glob.glob(f"{file_path}/**/{slug}.yml", recursive=True)
            if not len(blog_paths):
                return None
            file_path = blog_paths[0]
        else:
            file_path += ".yml"

        page_content = self._load_page_content(file_path)
        if page_content is None:
            return None
        if "stream_fields" not in page_content["content"]:
            return page_content
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
            elif "src" in sf:
                sf["src"] = self._patch_asset_in_src_sf(sf["src"])
        serialized_sf = self._serialize_divs_in_content(page_content)
        page_content["content"]["stream_fields"] = serialized_sf
        return page_content


class Html4PageHandler(BasePageHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa

    def initialize(self, **kwargs):
        super().initialize(**kwargs)

    def get(self, type_, section, *path_args):
        config_file = self.server_config["site_config_file"]
        if type_ not in self.site_config["config"]["types"]:
            return self._error(400, 'BadParameter', 'Parameter type {0} is unknown'.format(type_))
        if not self._check_par("section", section):
            return
        sub_section, slug = '', ''
        type_config = self.site_config["config"]["types"][type_]
        if "blog_index_type" not in type_config:
            if len(path_args) > 0:
                sub_section = path_args[0]
        else:
            if len(path_args) > 1:
                sub_section = path_args[0]
                slug = path_args[1]
            else:
                slug = path_args[0]

        self.logger.debug(f"GET: site_config_file {config_file} type '{type_}' section '{section}' sub_section '{sub_section}' slug '{slug}'")  # noqa
        page_content = self._get_page_content(section, sub_section, slug)
        if not page_content:
            return self._error(404, 'ResourceNotFound', 'The page content is missing')
        h4c = self.j24bots_loader.load(page_content, "page.j2")
        return self.finish(h4c)


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
        if slug:
            blox_page_content = self._get_page_content(section, sub_section, '')
            if not blox_page_content:
                return self._error(404, 'ResourceNotFound', 'The blog index content is missing')
            if "brand" in blox_page_content["content"] and "labels" in blox_page_content["content"]["brand"]:
                if "brand" not in page_content["content"]:
                    page_content["content"]["brand"] = {}
                page_content["content"]["brand"]["labels"] = blox_page_content["content"]["brand"]["labels"]
        type_config = self.site_config["config"]["types"][type_]
        if "blog_type" in type_config or "blog_index_type" in type_config:
            blog_index_type = type_ if "blog_type" in type_config else type_config["blog_index_type"]
            page_content["content"]["index_url"] = f"/{blog_index_type}/{section}/{sub_section}"
        self.write(json.dumps(page_content, indent=2))
        return self.finish()


class BlogsHandler(BasePageHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa

    def initialize(self, **kwargs):
        super().initialize(**kwargs)

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


class SiteMapHandler(BaseHandler):
    logger = logging.getLogger(__module__ + '.' + __qualname__)  # noqa

    def initialize(self, **kwargs):
        super().initialize(**kwargs)

    def _has_sub_menu(self, page):
        if "children" not in page:
            return False
        for child in page["children"]:
            if "menu" in child:
                return True
        return False

    def _get_page_content(self, section, sub_section, slug):
        file_path = self.server_config["pages_directory"]
        if file_path[-1] != "/":
            file_path += "/"
        file_path += section
        if sub_section:
            file_path += "/"
            file_path += sub_section
        if slug:
            blog_paths = glob.glob(f"{file_path}/**/{slug}.yml", recursive=True)
            if not len(blog_paths):
                return None
            file_path = blog_paths[0]
        else:
            file_path += ".yml"

        page_content = self._load_page_content(file_path)
        return page_content

    def _get_lastmod(self, meta):
        def i2s(s):
            if type(s) is int:
                return str(s)
            return s

        try:
            if meta:
                if "last_update_date" in meta:
                    return datetime.datetime.strptime(i2s(meta["last_update_date"]), "%Y%m%d")
                elif "publication_date" in meta:
                    return datetime.datetime.strptime(i2s(meta["publication_date"]), "%Y%m%d")
            return datetime.date.fromtimestamp(0)
        except ValueError:
            return datetime.date.fromtimestamp(0)

    def _get_urls(self, url_set, page, parent=None):
        if parent is None:
            loc = f"/{page['type']}/{page['id']}"
            page_content = self._get_page_content(page['id'], None, None)
            section = page['id']
            sub_section = None
        else:
            loc = f"/{page['type']}/{parent['id']}/{page['id']}"
            page_content = self._get_page_content(parent['id'], page['id'], None)
            section = parent['id']
            sub_section = page['id']
        page_date = self._get_lastmod(page_content["meta"] if page_content else None)

        url_set.append(
            {
                "loc": loc,
                "lastmod": page_date.strftime("%Y-%m-%d")
            }
        )
        type_config = self.site_config["config"]["types"][page['type']]
        if "blog_type" not in type_config:
            return
        blogs = self._get_blogs_index(section, sub_section)
        for blog in blogs:
            slug = blog["slug"]
            if parent is None:
                blog_loc = f"/{type_config['blog_type']}/{page['id']}/{slug}"
            else:
                blog_loc = f"/{type_config['blog_type']}/{parent['id']}/{page['id']}/{slug}"
            blog_date = self._get_lastmod(blog)
            url_set.append(
                {
                    "loc": blog_loc,
                    "lastmod": blog_date.strftime("%Y-%m-%d")
                }
            )

    def get(self, *path_args):
        url_set = []
        for page in self.site_config["pages"]:
            if "type" in page:
                self._get_urls(url_set, page)
            if not self._has_sub_menu(page):
                continue
            for child in page["children"]:
                if "menu" not in child:
                    continue
                self._get_urls(url_set, child, page)
        self.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        self.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        sitemap_root = self.server_config["sitemap_root"] if "sitemap_root" in self.server_config else ""

        for url in url_set:
            self.write('<url>')
            self.write(f'<loc>{sitemap_root}{url["loc"]}</loc>')
            self.write(f'<lastmod>{url["lastmod"]}</lastmod>')
            self.write('</url>\n')
        self.write('</urlset>\n')

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
        j24bots_loader = otvl_web.j24bots.Jinja2Loader(server_config["j24bots_directory"])

    handler_kwa = {
        "server_config": server_config,
        "site_config": site_config,
        "j24bots_loader": j24bots_loader
        }
    assets_directory = server_config["assets_directory"]
    return tornado.web.Application([
        (r"/api/version/?", VersionHandler, handler_kwa),
        (r"/api/sitemap.xml", SiteMapHandler, handler_kwa),
        (r"/api/site/config/?", SiteHandler, handler_kwa),
        (r"/api/site/pages/?", SiteHandler, handler_kwa),
        (r"/api/assets/(.*)", NoCacheStaticFileHandler, {"path": assets_directory}),
        (r"/api/blogs/([^/]*)/([^/]*)/([^/]*)/?", BlogsHandler, handler_kwa),
        (r"/api/blogs/([^/]*)/([^/]*)/?", BlogsHandler, handler_kwa),
        (r"/api/blogs/([^/]*)/?", BlogsHandler, handler_kwa),
        (r"/api/html4/([^/]*)/([^/]*)/([^/]*)/([^/]*)/?", Html4PageHandler, handler_kwa),
        (r"/api/html4/([^/]*)/([^/]*)/([^/]*)/?", Html4PageHandler, handler_kwa),
        (r"/api/html4/([^/]*)/([^/]*)/?", Html4PageHandler, handler_kwa),
        (r"/api/([^/]*)/([^/]*)/([^/]*)/([^/]*)/?", PageHandler, handler_kwa),
        (r"/api/([^/]*)/([^/]*)/([^/]*)/?", PageHandler, handler_kwa),
        (r"/api/([^/]*)/([^/]*)/?", PageHandler, handler_kwa),
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
