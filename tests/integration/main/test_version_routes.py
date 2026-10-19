"""
Test routes for version route, app/main/routes
"""
from importlib import reload

from app import create_app, db
import app.config as config_module


def test_version_route_default(client):
    """
    Test default version response when env is not set.
    """
    response = client.get('/version')
    assert response.status_code == 200
    assert response.data == b'unknown'


def test_version_route_set_env(monkeypatch):
    """
    Test version response when APP_VERSION is set.
    """
    monkeypatch.setenv('APP_VERSION', '11.0.0')
    reload(config_module)

    test_app = create_app(config_module.TestConfig)
    app_context = test_app.app_context()
    app_context.push()
    db.create_all()

    client = test_app.test_client()
    response = client.get('/version')

    assert response.status_code == 200
    assert response.data == b'11.0.0'

    db.session.remove()
    db.drop_all()
    app_context.pop()

    monkeypatch.delenv('APP_VERSION', raising=False)
    reload(config_module)
