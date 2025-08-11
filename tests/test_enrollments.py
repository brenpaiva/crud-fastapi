import pytest
from httpx import AsyncClient


@pytest.fixture
async def age_group_id(client: AsyncClient, auth_token: str):
    payload = {"name": "Infantil", "min_age": 10, "max_age": 15}
    r = await client.post("/age-groups/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 201
    return r.json()["id"]


@pytest.mark.asyncio
async def test_create_enrollment(client: AsyncClient, auth_token: str):
    payload_age_group = {"name": "Infantil", "min_age": 10, "max_age": 15}
    r_age_group = await client.post("/age-groups/", json=payload_age_group, headers={"Authorization": f"Bearer {auth_token}"})
    assert r_age_group.status_code == 201
    age_group_id = r_age_group.json()["id"]
    
    payload = {
        "name": "Joao", 
        "email": "joao@test.com",
        "age": 12, 
        "age_group_id": age_group_id
    }
    r = await client.post("/enrollments/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_list_enrollments(client: AsyncClient, auth_token: str):
    r = await client.get("/enrollments/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.asyncio
async def test_update_enrollment_status(client: AsyncClient, auth_token: str):
    payload_age_group = {"name": "Juvenil", "min_age": 13, "max_age": 17}
    r_age_group = await client.post("/age-groups/", json=payload_age_group, headers={"Authorization": f"Bearer {auth_token}"})
    assert r_age_group.status_code == 201
    age_group_id = r_age_group.json()["id"]
    
    payload = {
        "name": "Maria", 
        "email": "maria@test.com",
        "age": 13, 
        "age_group_id": age_group_id
    }
    r_create = await client.post("/enrollments/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert r_create.status_code == 201
    eid = r_create.json()["id"]

    r_upd = await client.patch(f"/enrollments/{eid}/status", params={"new_status": "approved"}, headers={"Authorization": f"Bearer {auth_token}"})
    assert r_upd.status_code == 200
    assert r_upd.json()["status"] == "approved"


@pytest.mark.asyncio
async def test_put_enrollment(client: AsyncClient, auth_token: str):
    payload_age_group = {"name": "Teen", "min_age": 14, "max_age": 16}
    r_age_group = await client.post("/age-groups/", json=payload_age_group, headers={"Authorization": f"Bearer {auth_token}"})
    assert r_age_group.status_code == 201
    age_group_id = r_age_group.json()["id"]
    
    payload = {
        "name": "Ana", 
        "email": "ana@test.com",
        "age": 14, 
        "age_group_id": age_group_id
    }
    r_create = await client.post("/enrollments/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert r_create.status_code == 201
    eid = r_create.json()["id"]

    upd_payload = {
        "name": "Ana Paula", 
        "email": "ana.paula@test.com",
        "age": 14, 
        "age_group_id": age_group_id
    }
    r_upd = await client.put(f"/enrollments/{eid}", json=upd_payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert r_upd.status_code == 200
    assert r_upd.json()["name"] == "Ana Paula"


@pytest.mark.asyncio
async def test_delete_enrollment(client: AsyncClient, auth_token: str):
    payload_age_group = {"name": "Young", "min_age": 15, "max_age": 18}
    r_age_group = await client.post("/age-groups/", json=payload_age_group, headers={"Authorization": f"Bearer {auth_token}"})
    assert r_age_group.status_code == 201
    age_group_id = r_age_group.json()["id"]
    
    payload = {
        "name": "Temp", 
        "email": "temp@test.com",
        "age": 15, 
        "age_group_id": age_group_id
    }
    r_create = await client.post("/enrollments/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert r_create.status_code == 201
    eid = r_create.json()["id"]
    r_del = await client.delete(f"/enrollments/{eid}", headers={"Authorization": f"Bearer {auth_token}"})
    assert r_del.status_code == 204
    r_get = await client.get(f"/enrollments/{eid}")
    assert r_get.status_code == 404
