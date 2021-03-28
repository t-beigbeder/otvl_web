import os
import glob
import logging

from fastapi import Path, HTTPException, status

from otvl_web.content import BaseFetcher, ContentFetcher


class IndexFetcher(BaseFetcher):
    logger = logging.getLogger(__name__)

    def __init__(self,
                 uri: str = Path(None, description="URI path for the requested index")
                 ):
        BaseFetcher.__init__(self, uri)

    def _get_content_dir(self):
        path = f"{self.ctx.content_path}/{self.uri}.yml"
        if os.path.exists(path):
            return os.path.dirname(path)
        dirs = self.uri.split("/")
        if len(dirs) < 2:
            return None
        gpath = f"{self.ctx.content_path}/{'/'.join(dirs[0:-1])}/**/{dirs[-1]}.yml"
        paths = glob.glob(gpath, recursive=True)
        if not paths:
            return None
        content_dir = os.path.dirname(paths[0])
        if not os.path.exists(content_dir):
            return None
        return content_dir

    def _get_index(self, content_dir):
        base_date = "19000101"

        def _get_sort_value(entry):
            date = base_date
            if "meta" in entry:
                date = str(entry["meta"].get("publication_date", base_date))
            return date

        index = []
        paths = glob.glob(f"{content_dir}/{os.path.basename(self.uri)}/**/*.yml", recursive=True)
        for entry_path in paths:
            entry_name = os.path.basename(entry_path)[0:-len(".yml")]
            entry_fetcher = ContentFetcher(f"{self.uri}/{entry_name}")
            entry_file_content = entry_fetcher.load_file_content(self.ctx)
            if entry_file_content is None:
                continue
            entry = {"name": entry_name}
            if "meta" in entry_file_content:
                entry["meta"] = entry_file_content["meta"]
            index.append(entry)
        index2 = sorted(index, key=lambda entry: entry.get("name", ""))
        index3 = sorted(index2, key=_get_sort_value, reverse=True)

        return {"index": index3}

    def fetch(self, ctx):
        self.ctx = ctx
        content_dir = self._get_content_dir()
        if content_dir is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return self._get_index(content_dir)
