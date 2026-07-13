import uuid
from datetime import datetime, timedelta, timezone


async def test_create_api_key_success(client, created_client, created_scope):
    response = await client.post(
        f"/clients/{created_client}/api-keys",
        json={"name": "test key", "scope_codes": ["read"], "expires_at": None},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["scopes"] == ["read"]
    assert "raw_key" in data
    assert data["status"] == "active"


async def test_create_api_key_with_expires_at(client, created_client, created_scope):
    expires = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()

    response = await client.post(
        f"/clients/{created_client}/api-keys",
        json={"name": "test key", "scope_codes": ["read"], "expires_at": expires},
    )

    assert response.status_code == 201


async def test_create_api_key_client_not_found(client, created_scope):
    fake_client_id = str(uuid.uuid4())

    response = await client.post(
        f"/clients/{fake_client_id}/api-keys",
        json={"name": "key", "scope_codes": ["read"], "expires_at": None},
    )

    assert response.status_code == 404


async def test_create_api_key_scope_not_found(client, created_client):
    response = await client.post(
        f"/clients/{created_client}/api-keys",
        json={"name": "key", "scope_codes": ["nonexistent"], "expires_at": None},
    )

    assert response.status_code == 404


async def test_create_api_key_inactive_client_returns_400(
    client, created_client, created_scope
):
    await client.patch(
        f"/clients/{created_client}", json={"is_active": False, "name": None}
    )

    response = await client.post(
        f"/clients/{created_client}/api-keys",
        json={"name": "key", "scope_codes": ["read"], "expires_at": None},
    )

    assert response.status_code == 400


async def test_list_api_keys_by_client(client, created_client, created_scope):
    await client.post(
        f"/clients/{created_client}/api-keys",
        json={"name": "key1", "scope_codes": ["read"], "expires_at": None},
    )

    response = await client.get(f"/clients/{created_client}/api-keys")

    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_revoke_api_key(client, created_client, created_scope):
    created = await client.post(
        f"/clients/{created_client}/api-keys",
        json={"name": "key", "scope_codes": ["read"], "expires_at": None},
    )
    key_id = created.json()["id"]

    response = await client.post(f"/api-keys/{key_id}/revoke")

    assert response.status_code == 200
    assert response.json()["status"] == "revoked"


async def test_revoke_already_revoked_key_returns_400(
    client, created_client, created_scope
):
    created = await client.post(
        f"/clients/{created_client}/api-keys",
        json={"name": "key", "scope_codes": ["read"], "expires_at": None},
    )
    key_id = created.json()["id"]
    await client.post(f"/api-keys/{key_id}/revoke")

    response = await client.post(f"/api-keys/{key_id}/revoke")

    assert response.status_code == 400


async def test_verify_api_key_success(client, created_client, created_scope):
    created = await client.post(
        f"/clients/{created_client}/api-keys",
        json={"name": "key", "scope_codes": ["read"], "expires_at": None},
    )
    raw_key = created.json()["raw_key"]

    response = await client.post("/api-keys/verify", json={"raw_key": raw_key})

    assert response.status_code == 200
    assert response.json()["scopes"] == ["read"]


async def test_verify_invalid_api_key_returns_401(client):
    response = await client.post(
        "/api-keys/verify", json={"raw_key": "invalid_key_xyz"}
    )
    assert response.status_code == 401


async def test_verify_revoked_api_key_returns_401(
    client, created_client, created_scope
):
    created = await client.post(
        f"/clients/{created_client}/api-keys",
        json={"name": "key", "scope_codes": ["read"], "expires_at": None},
    )
    key_id = created.json()["id"]
    raw_key = created.json()["raw_key"]
    await client.post(f"/api-keys/{key_id}/revoke")

    response = await client.post("/api-keys/verify", json={"raw_key": raw_key})

    assert response.status_code == 401
