def test_home_route(client):
    """Test the GET / route"""
    response = client.get("/")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["status"] == "success"
    assert json_data["message"] == "hello world!"


def test_echo_route(client):
    """Test the POST /echo route"""
    payload = {"name": "Raphael"}
    response = client.post("/echo", json=payload)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["status"] == "success"
    assert json_data["data"] == payload


def test_404_route(client):
    """Test non-existent route returns JSON 404"""
    response = client.get("/doesnotexist")
    json_data = response.get_json()

    assert response.status_code == 404
    assert json_data["status"] == "error"
    assert json_data["message"] == "not found"
