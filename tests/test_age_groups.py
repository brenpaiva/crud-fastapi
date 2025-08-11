import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_get_age_group(client: AsyncClient, auth_token: str):
    payload = {"name": "Sub-10", "min_age": 0, "max_age": 10}
    r = await client.post("/age-groups/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 201, r.text
    created = r.json()
    age_group_id = created["id"]

    r_list = await client.get("/age-groups/")
    assert r_list.status_code == 200
    assert any(ag["id"] == age_group_id for ag in r_list.json())

    r_get = await client.get(f"/age-groups/{age_group_id}")
    assert r_get.status_code == 200
    assert r_get.json()["name"] == "Sub-10"


@pytest.mark.asyncio
async def test_update_age_group(client: AsyncClient, auth_token: str):
    payload = {"name": "Adulto", "min_age": 18, "max_age": 60}
    r = await client.post("/age-groups/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 201
    ag = r.json()
    ag_id = ag["id"]

    update_payload = {"name": "Adulto Pleno"}
    r_upd = await client.put(f"/age-groups/{ag_id}", json=update_payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert r_upd.status_code == 200, r_upd.text
    assert r_upd.json()["name"] == "Adulto Pleno"


@pytest.mark.asyncio
async def test_delete_age_group(client: AsyncClient, auth_token: str):
    payload = {"name": "Temp", "min_age": 5, "max_age": 7}
    r = await client.post("/age-groups/", json=payload, headers={"Authorization": f"Bearer {auth_token}"})
    assert r.status_code == 201
    ag_id = r.json()["id"]
    r_del = await client.delete(f"/age-groups/{ag_id}", headers={"Authorization": f"Bearer {auth_token}"})
    assert r_del.status_code == 204
    r_get = await client.get(f"/age-groups/{ag_id}")
    assert r_get.status_code == 404
