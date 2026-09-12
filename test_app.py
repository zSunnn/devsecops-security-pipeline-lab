from app import app

def test_welcome():
    client = app.test_client()
    response = client.get("/welcome")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "You reached the hello route"

def test_old_hello_route_not_found():
    client = app.test_client()
    response = client.get("/hello")
    assert response.status_code == 404