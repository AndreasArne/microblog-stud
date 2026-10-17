"""
Test routes for app version information.
"""


def test_version_route_default_value(client):
    """
    Test default application version value.
    """
    response = client.get('/version')
    assert response.status_code == 200
    assert response.data == b'unknown'


def test_version_route_with_configured_value(client, test_app):
    """
    Test configured application version value.
    """
    test_app.config['APP_VERSION'] = '11.0.0'
    response = client.get('/version')
    assert response.status_code == 200
    assert response.data == b'11.0.0'
