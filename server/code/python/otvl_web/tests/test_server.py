import logging
import sys
import os
import json

import pytest
import yaml

import otvl_web.server


logger = logging.getLogger(__name__)


def body_to_obj(json_bytes):
    return json.loads(json_bytes.decode("utf-8"))


@pytest.fixture(autouse=True)
def env_setup(monkeypatch):
    sys.argv = ["main"]
    monkeypatch.setenv('LOGGING', 'INFO')
    monkeypatch.setenv('CONFIG_DIR', 'data/tests')
    monkeypatch.setenv('CONFIG_NAME', 'test_server_site1')


@pytest.fixture
def app():
    config_dir = os.getenv('CONFIG_DIR', 'code/config')
    config_name = os.getenv('CONFIG_NAME', "undefined_config_name") + '.yml'
    with open(f"{config_dir}/{config_name}") as ysd:
        config = yaml.load(ysd, Loader=yaml.FullLoader)
    return otvl_web.server.make_otvl_web_app(config)


@pytest.mark.gen_test
def test_hello_world(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200


@pytest.mark.gen_test
def test_get_site_config(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/site/config/")
    assert response.code == 200
    resp_o = body_to_obj(response.body)
    assert resp_o["home_section"] == "home" and len(resp_o["types"]) == 3


@pytest.mark.gen_test
def test_get_site_pages(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/site/pages/")
    assert response.code == 200
    resp_o = body_to_obj(response.body)
    assert resp_o[0]["id"] == "home"


if __name__ == "__main__":
    # pytest.main()
    pytest.main(['-v', '-s', '-k', 'test_server.py'])
