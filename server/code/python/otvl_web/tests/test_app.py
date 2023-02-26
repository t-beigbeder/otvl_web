from os import getenv as the_real_getenv
from unittest.mock import patch
import logging
import os
import xml.etree.ElementTree as ET

import pytest

from fastapi import status

from otvl_web.app import BASE_URL
from otvl_web.context import Context


logging.basicConfig(
    level=os.getenv('LOGGING', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def test_context():
    def os_getenv(*args, **kwargs):
        if args[0] == "OTVL_WEB_HOST":
            return "127.0.0.3"
        if args[0] == "OTVL_WEB_PORT":
            return "9393"
        if args[0] == "OTVL_WEB_RELOAD":
            return "1"
        if args[0] == "OTVL_WEB_INSECURE_CORS":
            return "1"
        if args[0] == "OTVL_WEB_CONFIG_PATH":
            return "config3.yml"
        return the_real_getenv(*args, **kwargs)

    c = Context()
    assert c.host == "127.0.0.1"
    c2 = Context(host="127.0.0.2")
    assert c2.host == "127.0.0.2"
    with patch("os.getenv", side_effect=os_getenv):
        c3 = Context()
        assert c3.host == "127.0.0.3"
        assert c3.config_path == "config3.yml"
        assert c3.port == 9393
        assert c3.reload is True
        assert c3.insecure_cors is True


def test_context_config(test_config, monkeypatch):
    c = Context()
    assert c.config_path == "otvl_web_config.yml"
    assert c.content_path == "content"
    c2 = Context(content_path="data/tests/content2")
    assert c2.content_path == "data/tests/content2"
    monkeypatch.setenv("OTVL_WEB_CONTENT_PATH", "data/tests/content3")
    c3 = Context()
    assert c3.content_path == "data/tests/content3"


def test_version(client):
    response = client.get(f"{BASE_URL}/version")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['version'] == '2.0.0'


def test_get_config(client):
    response = client.get(f"{BASE_URL}/config")
    assert response.status_code == status.HTTP_200_OK
    oresp = response.json()
    assert 'vuejs' in oresp
    assert 'server' not in oresp


@pytest.mark.parametrize("uri", ["c1", "tc/c2", "tc/c3", "tc/c3/"])
def test_get_content(client, uri):
    response = client.get(f"{BASE_URL}/content/{uri}")
    assert response.status_code == status.HTTP_200_OK
    oresp = response.json()
    assert oresp["content"] is not None


def test_get_no_content(client):
    uri = "cnc"
    response = client.get(f"{BASE_URL}/content/{uri}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_bad_content(client):
    uri = "cbc"
    response = client.get(f"{BASE_URL}/content/{uri}")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
def test_blog_index(client):
    uri = "blog"
    response = client.get(f"{BASE_URL}/content/{uri}")
    assert response.status_code == status.HTTP_200_OK
    oresp = response.json()
    assert oresp["meta"]["creation_date"] == "20200528"
    assert len(oresp["content"]["stream_fields"]) == 3


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
def test_blog_article(client):
    uri = "blog/minikube"
    response = client.get(f"{BASE_URL}/content/{uri}")
    assert response.status_code == status.HTTP_200_OK
    oresp = response.json()
    assert len(oresp["content"]["stream_fields"]) == 5


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
def test_get_content_sf4(client):
    response = client.get(f"{BASE_URL}/content/c4-sf")
    assert response.status_code == status.HTTP_200_OK
    oresp = response.json()
    assert oresp["content"] is not None
    assert oresp["content"]["title"] == "TitleC4Sf"
    assert oresp["content"]["heading"] == "Heading C4Sf"
    assert len(oresp["content"]["stream_fields"]) == 3
    sfs = oresp["content"]["stream_fields"]
    assert sfs[0]["type"] == "html"
    assert ">h1 in emd<" in sfs[0]["content"]
    assert sfs[1]["type"] == "html"
    assert ">heading in md_data<" in sfs[1]["content"]
    assert "<p>Text in md_data</p>" in sfs[1]["content"]
    assert "href=\"http://otvl-dev-host:9090/api/v2/asset/images/home/nature.jpg\"" in sfs[1]["content"]
    assert sfs[2]["type"] == "sf_img_in_card"
    assert sfs[2]["src"] == "http://otvl-dev-host:9090/api/v2/asset/images/home/nature.jpg"


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
def test_get_content_sf_nofile(client):
    response = client.get(f"{BASE_URL}/content/c5-sf-nofile")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    oresp = response.json()
    assert oresp["detail"] == "missing content"


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
def test_get_asset_ok(client):
    response = client.get(f"{BASE_URL}/asset/images/common/agpl-logo-120x32.jpg")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
def test_get_asset_nok(client):
    response = client.get(f"{BASE_URL}/asset/images/common/agpl-logo-120x32x19.jpg")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("uri", ["c1", "tc/c2", "tc/c3", "tc/c3/"])
def test_get_index_empty(client, uri):
    response = client.get(f"{BASE_URL}/index/{uri}")
    assert response.status_code == status.HTTP_200_OK
    oresp = response.json()
    assert len(oresp["index"]) == 0


def test_get_index_sort(client):
    uri = "xp"
    response = client.get(f"{BASE_URL}/index/{uri}")
    assert response.status_code == status.HTTP_200_OK
    oresp = response.json()
    assert len(oresp["index"]) == 5
    assert [entry["name"] for entry in oresp["index"]] == ['xp3', 'xp1', 'xp2', 'xpa', 'xpb']


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
def test_get_index_blog(client):
    uri = "blog"
    response = client.get(f"{BASE_URL}/index/{uri}")
    assert response.status_code == status.HTTP_200_OK
    oresp = response.json()
    assert len(oresp["index"]) == 7


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
def test_get_index_about(client):
    uri = "about"
    response = client.get(f"{BASE_URL}/index/{uri}")
    assert response.status_code == status.HTTP_200_OK
    oresp = response.json()
    assert len(oresp["index"]) == 1


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
def test_get_sitemap(client):
    response = client.get(f"{BASE_URL}/sitemap.xml")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/xml"
    urlset = ET.fromstring(response.text)
    urls = list(urlset.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url"))
    assert len(urls) == 14


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
def test_blog_article_as_html(client):
    uri = "blog/minikube"
    response = client.get(f"{BASE_URL}/html/{uri}")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
def test_404_as_html(client):
    uri = "blog/minikube2"
    response = client.get(f"{BASE_URL}/html/{uri}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize('test_config', ['unit_test_server02'])
@pytest.mark.parametrize('uri', ['', '/'])
def test_home_redirect_as_html(client, uri):
    response = client.get(f"{BASE_URL}/html{uri}")
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]


if __name__ == '__main__':
    # pytest.main()
    pytest.main(['-v', '-s', '-k', 'test_app.py'])
    # pytest.main(['-v', '-s', '-k', 'test_home_redirect_as_html'])
