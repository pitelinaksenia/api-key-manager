import uuid


async def test_create_client(client):
    response = await client.post(
        "/clients/", json={"name": "Acme", "email": "acme@test.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Acme"
    assert data["email"] == "acme@test.com"
    assert data["is_active"] is True
    assert "id" in data


async def test_create_client_duplicate_email_returns_409(client):
    await client.post("/clients/", json={"name": "Acme", "email": "acme@test.com"})

    response = await client.post(
        "/clients/", json={"name": "Other", "email": "acme@test.com"}
    )

    assert response.status_code == 409


async def test_get_all_clients_empty(client):
    response = await client.get("/clients/")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_all_clients_returns_created(client):
    await client.post("/clients/", json={"name": "A", "email": "a@test.com"})
    await client.post("/clients/", json={"name": "B", "email": "b@test.com"})

    response = await client.get("/clients/")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_client_by_id(client, created_client):
    response = await client.get(f"/clients/{created_client}")
    assert response.status_code == 200
    assert response.json()["name"] == "Acme"


async def test_get_client_not_found(client):
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/clients/{fake_id}")
    assert response.status_code == 404


async def test_update_client_name(client, created_client):
    response = await client.patch(
        f"/clients/{created_client}", json={"name": "New Name", "is_active": None}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
    assert response.json()["email"] == "acme@test.com"


async def test_update_client_not_found(client):
    fake_id = str(uuid.uuid4())
    response = await client.patch(
        f"/clients/{fake_id}", json={"name": "X", "is_active": None}
    )
    assert response.status_code == 404
