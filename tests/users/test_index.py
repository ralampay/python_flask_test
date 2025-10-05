def test_index(client, mock_user):
    """
    Ensure GET /api/users returns a list of users 
    and includes the mock user.
    """
    response = client.get("/users")
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)
    assert any(u["email"] == mock_user.email for u in data["data"])
