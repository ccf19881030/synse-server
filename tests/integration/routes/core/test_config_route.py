"""Test the 'synse.routes.core' Synse Server module's config route."""
# pylint: disable=redefined-outer-name,unused-argument

import pytest
import ujson

from synse import config, factory
from synse.version import __api_version__

config_url = '/synse/{}/config'.format(__api_version__)


@pytest.fixture()
def app():
    """Fixture to get a Synse Server application instance."""
    # Need to reset default configuration filepath
    # because the path in test environment is different
    config.DEFAULT_CONFIG_PATH = '/code/config/config.yml'

    # Load configuration options
    config.load()

    yield factory.make_app()


def test_config_endpoint_ok(app):
    """Test getting a good config response.

    Details:
        These are the final configurations for the application.
        Check one by one to to make sure it return the right value.
    """
    _, response = app.test_client.get(config_url)

    assert response.status == 200

    data = ujson.loads(response.text)

    assert 'locale' in data
    assert 'pretty_json' in data
    assert 'logging' in data
    assert 'cache' in data
    assert 'grpc' in data

    assert data['locale'] == 'en_US'
    assert data['pretty_json'] == True
    assert data['logging'] == 'debug'
    assert data['cache'] == {'meta': {'ttl': 20}, 'transaction': {'ttl': 20}}
    assert data['grpc'] == {'timeout': 20}


def test_config_endpoint_post_not_allowed(app):
    """Invalid request: POST"""
    _, response = app.test_client.post(config_url)
    assert response.status == 405


def test_config_endpoint_put_not_allowed(app):
    """Invalid request: PUT"""
    _, response = app.test_client.put(config_url)
    assert response.status == 405


def test_config_endpoint_delete_not_allowed(app):
    """Invalid request: DELETE"""
    _, response = app.test_client.delete(config_url)
    assert response.status == 405


def test_config_endpoint_patch_not_allowed(app):
    """Invalid request: PATCH"""
    _, response = app.test_client.patch(config_url)
    assert response.status == 405


def test_config_endpoint_head_not_allowed(app):
    """Invalid request: HEAD"""
    _, response = app.test_client.head(config_url)
    assert response.status == 405


def test_config_endpoint_options_not_allowed(app):
    """Invalid request: OPTIONS"""
    _, response = app.test_client.options(config_url)
    assert response.status == 405
