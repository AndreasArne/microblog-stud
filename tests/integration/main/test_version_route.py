"""
Test route that shows the running version, app/main/routes
"""
# pylint: disable=redefined-outer-name,unused-argument

def test_version_route_without_login(client):
    """
    Test that the version is shown without logging in
    """
    response = client.get("/version")
    assert response.status_code == 200
    assert response.data == b"unknown"



def test_version_route_shows_configured_version(client, test_app):
    """
    Test that the version from the config is shown
    """
    test_app.config["APP_VERSION"] = "11.0.1"
    response = client.get("/version")
    assert response.status_code == 200
    assert response.data == b"11.0.1"
