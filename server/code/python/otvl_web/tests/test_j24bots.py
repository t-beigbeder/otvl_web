import logging
import sys
import os

import pytest
import yaml

import otvl_web.j24bots


logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    sys.argv = ["main"]
    monkeypatch.setenv('LOGGING', 'INFO')
    monkeypatch.setenv('CONFIG_DIR', 'data/tests')
    monkeypatch.setenv('CONFIG_NAME', 'test_unit_server_site1')


def get_j2dir():
    config_dir = os.getenv('CONFIG_DIR')
    config_name = os.getenv('CONFIG_NAME') + '.yml'
    config_file = f"{config_dir}/{config_name}"
    with open(config_file) as ysd:
        server_config = yaml.load(ysd, Loader=yaml.FullLoader)
        return server_config["j24bots_directory"]


def test_j24bots_loader(monkeypatch):
    j2l = otvl_web.j24bots.Jinja2Loader(get_j2dir())
    rendered = j2l.load({"title": "test_j24bots_loader"}, "test_page.j2")
    assert "<title>test_j24bots_loader</title>" in rendered


if __name__ == "__main__":
    # pytest.main()
    pytest.main(['-v', '-s', '-k', 'test_j24bots.py'])
