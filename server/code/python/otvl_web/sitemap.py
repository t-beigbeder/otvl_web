import logging
import os
import os.path
from io import StringIO
import re
import datetime

from fastapi.responses import Response

from otvl_web.content import ContentFetcher


class SiteMapFetcher():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.ctx = None

    def _get_lastmod(self, meta):
        def i2s(s):
            if type(s) is int:
                return str(s)
            return s

        def dt2s(dt):
            return dt.strftime("%Y-%m-%d")

        try:
            if meta:
                if "last_update_date" in meta:
                    return dt2s(datetime.datetime.strptime(i2s(meta["last_update_date"]), "%Y%m%d"))
                elif "publication_date" in meta:
                    return dt2s(datetime.datetime.strptime(i2s(meta["publication_date"]), "%Y%m%d"))
            return dt2s(datetime.date.fromtimestamp(0))
        except ValueError:
            return dt2s(datetime.date.fromtimestamp(0))

    def _is_private(self, uri):
        if "private_uris" not in self.ctx.config["server"]:
            return False
        for private_uri in self.ctx.config["server"]["private_uris"]:
            if re.match(private_uri, uri):
                return True
        return False

    def _do_fetch(self, request):
        content = StringIO()
        content.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        content.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        docs = {"/": None}
        for dirpath, dirnames, filenames in os.walk(self.ctx.content_path):
            reldirpath = dirpath[len(self.ctx.content_path):] + "/"
            for filename in filenames:
                if not re.search("\\.yml$", filename):
                    continue
                docname = filename[:-len(".yml")]
                pathparts = reldirpath.split("/")
                for i in range(len(reldirpath)):
                    curpath = "/".join(pathparts)
                    if curpath in docs:
                        docs[os.path.join(curpath, docname)] = None
                        break
                    pathparts = pathparts[:-1]
                else:
                    docs[f"{reldirpath}{docname}"] = None

        base_url = f"https://{request.base_url.hostname}/"
        for doc, path in docs.items():
            if doc == "/":
                continue
            if self._is_private(doc[1:]):
                continue
            entry_fetcher = ContentFetcher(doc[1:])
            entry_file_content = entry_fetcher.load_file_content(self.ctx)
            if entry_file_content is None:
                self.logger.error(f"fetch document {doc}: no known content")
                continue
            last_mod = self._get_lastmod(entry_file_content.get("meta"))
            content.write("\t<url>\n")
            content.write(f"\t\t<loc>{base_url}{doc[1:]}</loc>\n")
            content.write(f"\t\t<lastmod>{last_mod}</lastmod>\n")
            content.write("\t</url>")
        content.write("</urlset>")
        return content.getvalue().encode("utf-8")

    def fetch(self, request, ctx):
        self.ctx = ctx
        content = self._do_fetch(request)
        return Response(content=content, media_type="application/xml")
