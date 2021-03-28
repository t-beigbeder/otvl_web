import pytest
from fastapi.testclient import TestClient

from otvl_web.app import app as the_app
from otvl_web.app import get_ctx as the_get_ctx
from otvl_web import context


def override_get_ctx():
    return context.Context()


the_app.dependency_overrides[the_get_ctx] = override_get_ctx


@pytest.fixture(scope="function")
def test_config():
    return "unit_test_server01"


@pytest.fixture(scope="function")
def app(monkeypatch, test_config):
    monkeypatch.setenv("OTVL_WEB_CONFIG_PATH", f"data/tests/{test_config}/config.yml")
    yield the_app


@pytest.fixture(scope="function")
def client(app):
    client = TestClient(app)
    yield client
