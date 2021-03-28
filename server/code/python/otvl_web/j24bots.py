import logging

from jinja2 import Environment, FileSystemLoader, TemplateError


class Jinja2Loader():
    logger = logging.getLogger(__name__)

    def __init__(self, j2_dir):
        self.j2_dir = j2_dir

    def load(self, j2var, path):
        self.logger.debug(f"Loading template {path}")
        j2env = Environment(loader=FileSystemLoader(self.j2_dir))
        try:
            tmpl = j2env.get_template(path)
            rendered = tmpl.render(j2var)
            return rendered
        except TemplateError as te:
            self.logger.error(f"Jinja2 error while loading {path}: {te}")
            raise
