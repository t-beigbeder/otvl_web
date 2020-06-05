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
    monkeypatch.setenv('CONFIG_NAME', 'test_unit_server_site1')


@pytest.fixture
def app():
    config_dir = os.getenv('CONFIG_DIR', 'code/config')
    config_name = os.getenv('CONFIG_NAME', "undefined_config_name") + '.yml'
    with open(f"{config_dir}/{config_name}") as ysd:
        config = yaml.load(ysd, Loader=yaml.FullLoader)
    return otvl_web.server.make_otvl_web_app(config)


@pytest.mark.gen_test
def test_version(http_client, base_url):
    response = yield http_client.fetch(base_url + "/api/version")
    assert response.code == 200
    resp_o = body_to_obj(response.body)
    assert resp_o["server"] == "1.0"


@pytest.mark.gen_test
def test_get_site_config(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/api/site/config/")
    assert response.code == 200
    resp_o = body_to_obj(response.body)
    assert resp_o["home_section"] == "home" and len(resp_o["types"]) == 3
    assert resp_o["assets_url"] == "http://vjs-dev-host:8888/api/assets/"


@pytest.mark.gen_test
def test_get_site_pages(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/api/site/pages/")
    assert response.code == 200
    resp_o = body_to_obj(response.body)
    assert resp_o[0]["id"] == "home"


@pytest.mark.gen_test
def test_get_home_content(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/api/page/home/")
    assert response.code == 200
    assert response.headers["Content-Type"] == "application/json"
    resp_o = body_to_obj(response.body)
    assert "meta" in resp_o
    assert "content" in resp_o


@pytest.mark.gen_test
def test_get_incorrect_type(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/api/page2/home/", raise_error=False)
    assert response.code == 400
    resp_o = body_to_obj(response.body)
    assert resp_o["reason"] == "BadParameter"
    assert resp_o["message"] == "Parameter type page2 is unknown"


@pytest.mark.gen_test
def test_get_home_asset_content(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/api/page/home/")
    assert response.code == 200
    resp_o = body_to_obj(response.body)
    assert "stream_fields" in resp_o["content"]
    assert len(resp_o["content"]["stream_fields"]) == 3
    sf1c = resp_o["content"]["stream_fields"][0]["content"]
    ix = sf1c.index(" src=\"")
    asset_url = "http://vjs-dev-host:8888/api/assets/"
    assert sf1c[ix+6:].startswith(asset_url)
    sf2c = resp_o["content"]["stream_fields"][1]["content"]
    ix = sf2c.index(" href=\"")
    assert sf2c[ix+7:].startswith(asset_url)
    sf3s = resp_o["content"]["stream_fields"][2]["src"]
    assert sf3s.startswith(asset_url)


@pytest.mark.gen_test
def test_get_blogs_index(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/api/blogs/corporate-blog///", raise_error=False)
    assert response.code == 200
    resp_o = body_to_obj(response.body)
    assert "blogs" in resp_o
    assert len(resp_o["blogs"]) > 1


@pytest.mark.gen_test
def test_get_blogs_content(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/api/blox/corporate-blog/", raise_error=False)
    assert response.code == 200
    resp_o = body_to_obj(response.body)
    assert "meta" in resp_o
    assert "content" in resp_o
    assert resp_o["content"]["brand"]["labels"]["index_title"] == "List of corporate blogs"
    assert resp_o["content"]["index_url"] == "/blox/corporate-blog/"

    response = yield http_client.fetch(base_url + "/api/blogs/corporate-blog///", raise_error=False)
    assert response.code == 200
    resp_o = body_to_obj(response.body)
    assert "blogs" in resp_o

    assert len(resp_o["blogs"]) > 1
    for blog in resp_o["blogs"]:
        response = yield http_client.fetch(
            base_url + "/api/blog/corporate-blog//" + blog["slug"],
            raise_error=False)
        assert response.code == 200
        resp_o = body_to_obj(response.body)
        assert "meta" in resp_o
        assert "content" in resp_o
        if resp_o["content"]["title"] == "Blog 101 corporate":
            assert True
        assert resp_o["content"]["brand"]["labels"]["index_title"] == "List of corporate blogs"
        assert resp_o["content"]["index_url"] == "/blox/corporate-blog/"


@pytest.mark.gen_test
def test_get_sitemap(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/api/sitemap.xml", raise_error=False)
    assert response.code == 200
    assert response.headers["Content-Type"] == "text/xml; charset=utf-8"
    lines = response.body.decode("utf-8").split('\n')
    assert "urlset" in lines[1]
    assert len(lines) >= 6
    for line in lines[2:-2]:
        assert line.startswith("<url><loc>")
        assert line.endswith("</lastmod></url>")
        url = line[len("<url><loc>"):line.index("</loc")]
        lm = line[line.index("<lastmod>")+len("<lastmod>"):line.index("</lastmod")]
        assert len(url)
        if lm == "1970-01-01":
            continue
        # web omit empty blog subsection, API does not
        url_comps = url.split("/")
        type_ = url_comps[1]
        section = url_comps[2]
        api_url = f"/api/{type_}/{section}"
        sub_section, slug = '', ''
        if type_ != "blog":
            if len(url_comps) > 3:
                sub_section = url_comps[3]
                api_url = f"/api/{type_}/{section}/{sub_section}"
        else:
            if len(url_comps) <= 4:
                slug = url_comps[3]
            else:
                sub_section = url_comps[3]
                slug = url_comps[4]
            api_url = f"/api/{type_}/{section}/{sub_section}/{slug}"

        response = yield http_client.fetch(
            base_url + api_url,
            raise_error=False)
        assert response.code == 200
        assert response.headers["Content-Type"] == "application/json"


@pytest.mark.gen_test
def test_get_html_home_content(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/api/html4/page/home/", raise_error=False)
    assert response.code == 200
    assert response.headers["Content-Type"] == "text/html"
    body = response.body.decode("utf-8")
    assert "<title>Home for Otvl Web</title>" in body


@pytest.mark.gen_test
def test_get_sitemap_pages_as_html(http_client, base_url, caplog, monkeypatch):
    response = yield http_client.fetch(base_url + "/api/sitemap.xml", raise_error=False)
    assert response.code == 200
    lines = response.body.decode("utf-8").split('\n')
    assert "urlset" in lines[1]
    assert len(lines) >= 6
    for line in lines[2:-2]:
        assert line.startswith("<url><loc>")
        assert line.endswith("</lastmod></url>")
        url = line[len("<url><loc>"):line.index("</loc")]
        lm = line[line.index("<lastmod>")+len("<lastmod>"):line.index("</lastmod")]
        assert len(url)
        if lm == "1970-01-01":
            continue
        # web omit empty blog subsection, API does not
        url_comps = url.split("/")
        type_ = url_comps[1]
        section = url_comps[2]
        api_url = f"/api/html4/{type_}/{section}"
        sub_section, slug = '', ''
        if type_ != "blog":
            if len(url_comps) > 3:
                sub_section = url_comps[3]
                api_url = f"/api/html4/{type_}/{section}/{sub_section}"
        else:
            if len(url_comps) <= 4:
                slug = url_comps[3]
            else:
                sub_section = url_comps[3]
                slug = url_comps[4]
            api_url = f"/api/html4/{type_}/{section}/{sub_section}/{slug}"

        response = yield http_client.fetch(
            base_url + api_url,
            raise_error=False)
        assert response.code == 200
        assert response.headers["Content-Type"] == "text/html"
        body = response.body.decode("utf-8")  # noqa


if __name__ == "__main__":
    # pytest.main()
    pytest.main(['-v', '-s', '-k', 'test_server.py'])
