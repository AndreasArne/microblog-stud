"""Tests for the public version route."""
import importlib
from app import create_app
from app import config


def test_version_defaults_to_unknown(client):
    """A build without version metadata identifies itself as unknown."""
    response = client.get('/version')
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'unknown'
    assert response.mimetype == 'text/plain'


def test_version_from_environment(monkeypatch):
    """The application reads APP_VERSION from its environment."""
    with monkeypatch.context() as patcher:
        patcher.setenv('APP_VERSION', '11.0.0')
        importlib.reload(config)
        response = create_app(config.TestConfig).test_client().get('/version')
        assert response.status_code == 200
        assert response.get_data(as_text=True) == '11.0.0'
    importlib.reload(config)
