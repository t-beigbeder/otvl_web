import re

from fastapi import Path, HTTPException, status, Response

from otvl_web.content import BaseFetcher
from otvl_web.index import IndexFetcher
from otvl_web.j24bots import Jinja2Loader


class HtmlFetcher(BaseFetcher):
    def __init__(self,
                 uri: str = Path(None, description="URI path for the requested HTML")
                 ):
        BaseFetcher.__init__(self, uri)

    def fetch(self, ctx):
        self.ctx = ctx
        if not self.uri and "home_mapped_to" in self.ctx.config["server"]:
            self.uri = self.ctx.config["server"]["home_mapped_to"]
        file_content = self.do_load_file_content(ctx)
        if file_content is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        page_content = self._get_page_content(file_content)

        page_index = IndexFetcher(self.uri).fetch(ctx)
        j2var = {
            "uri": self.uri,
            "server_config": self.server_config(),
            **page_index,
            **page_content,
        }
        for j2t in self.ctx.config["server"]["j24bots_templates"]:
            if not re.match(j2t["uri"], self.uri):
                continue
            break
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        h4c = Jinja2Loader(self.ctx.j24bots_path).load(j2var, j2t["template"])
        return Response(content=h4c, media_type="text/html")
