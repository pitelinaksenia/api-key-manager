import uuid


async def test_create_scope(client):
    response = await client.post(
        "/scopes/", json={"code": "read", "description": "Read access"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "read"
    assert "id" in data


async def test_create_scope_duplicate_code_returns_409(client):
    await client.post("/scopes/", json={"code": "read", "description": "Read"})

    response = await client.post(
        "/scopes/", json={"code": "read", "description": "Different desc"}
    )

    assert response.status_code == 409


async def test_get_all_scopes_empty(client):
    response = await client.get("/scopes/")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_all_scopes_returns_created(client):
    await client.post("/scopes/", json={"code": "read", "description": "Read"})
    await client.post("/scopes/", json={"code": "write", "description": "Write"})

    response = await client.get("/scopes/")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_scope_by_id(client, created_scope):
    response = await client.get(f"/scopes/{created_scope}")
    assert response.status_code == 200
    assert response.json()["code"] == "read"


async def test_get_scope_not_found(client):
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/scopes/{fake_id}")
    assert response.status_code == 404
