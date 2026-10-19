"""
Test monitoring related routes.
"""

from app import create_app, db
from app.config import TestConfig


def test_metrics_route_available(client):
    """
    Test that metrics endpoint is available.
    """
    response = client.get('/metrics')

    assert response.status_code == 200
    assert b'flask_http_request_total' in response.data


def test_boom_route_returns_500_page():
    """
    Test that the synthetic error route triggers the custom 500 handler.
    """
    app = create_app(TestConfig)
    app.config.update(TESTING=False, PROPAGATE_EXCEPTIONS=False)

    app_context = app.app_context()
    app_context.push()
    db.create_all()

    try:
        client = app.test_client()
        response = client.get('/boom')
    finally:
        db.session.remove()
        db.drop_all()
        app_context.pop()

    assert response.status_code == 500
    assert b'An unexpected error has occurred' in response.data
