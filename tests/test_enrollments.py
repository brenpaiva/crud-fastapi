import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_enrollment(client: AsyncClient, auth_token: str):
	payload = {"name": "Joao", "age": 12, "cpf": "12345678901"}
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
	# cria
	payload = {"name": "Maria", "age": 20, "cpf": "12345678902"}
	r_create = await client.post("/enrollments/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
	assert r_create.status_code == 201
	eid = r_create.json()["id"]

	# update status
	r_upd = await client.patch(f"/enrollments/{eid}/status", params={"new_status": "approved"}, headers={"Authorization": f"Bearer {auth_token}"})
	assert r_upd.status_code == 200
	assert r_upd.json()["status"] == "approved"


@pytest.mark.asyncio
async def test_put_enrollment(client: AsyncClient, auth_token: str):
	payload = {"name": "Ana", "age": 30, "cpf": "12345678903"}
	r_create = await client.post("/enrollments/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
	assert r_create.status_code == 201
	eid = r_create.json()["id"]

	upd_payload = {"name": "Ana Paula", "age": 31, "cpf": "12345678903"}
	r_upd = await client.put(f"/enrollments/{eid}", json=upd_payload, headers={"Authorization": f"Bearer {auth_token}"})
	assert r_upd.status_code == 200
	assert r_upd.json()["name"] == "Ana Paula"


@pytest.mark.asyncio
async def test_delete_enrollment(client: AsyncClient, auth_token: str):
	payload = {"name": "Temp", "age": 15, "cpf": "12345678904"}
	r_create = await client.post("/enrollments/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
	assert r_create.status_code == 201
	eid = r_create.json()["id"]
	r_del = await client.delete(f"/enrollments/{eid}", headers={"Authorization": f"Bearer {auth_token}"})
	assert r_del.status_code == 204
	r_get = await client.get(f"/enrollments/{eid}")
	assert r_get.status_code == 404
