import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.config import settings
from app.db.session import get_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        from app.models import age_group
        from app.models import enrollment
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session_maker() as sess:
        yield sess


@pytest_asyncio.fixture(autouse=True)
async def override_db(session):
    async def _get_session_override():
        yield session
    app.dependency_overrides[get_session] = _get_session_override
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_redis_queue(monkeypatch):
    from app.queue import redis_backend
    calls: list[dict] = []

    async def fake_enqueue(payload: dict):
        calls.append(payload)

    async def fake_dequeue_batch(max_items: int):
        batch = calls[:max_items]
        del calls[:max_items]
        return batch

    monkeypatch.setattr(redis_backend.redis_queue, "enqueue", fake_enqueue)
    monkeypatch.setattr(redis_backend.redis_queue, "dequeue_batch", fake_dequeue_batch)
    yield


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def auth_token(client):
    data = {"username": settings.API_USERNAME, "password": settings.API_PASSWORD}
    resp = await client.post("/token", data=data)
    assert resp.status_code == 200
    return resp.json()["access_token"]


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
