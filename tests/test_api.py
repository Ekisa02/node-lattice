import pytest
from httpx import AsyncClient
from app.main import app
from app.core.model import ModelEngine
import asyncio

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        r = await ac.get('/health')
        assert r.status_code == 200
        j = r.json()
        assert 'status' in j

@pytest.mark.asyncio
async def test_predict_endpoint():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        payload = {"features": [0.1, 0.2, 0.3, 0.4]}
        r = await ac.post('/predict', json=payload)
        assert r.status_code == 200
        j = r.json()
        assert 'score' in j
        assert isinstance(j['score'], float)

@pytest.mark.asyncio
async def test_ingest_endpoint():
    async with AsyncClient(app=app, base_url='http://test') as ac:
        payload = {
            "hash": "0xdeadbeef",
            "from_addr": "0x1",
            "to_addr": "0x2",
            "value": 1000000000000000000,
            "gas": 21000,
            "timestamp": 1620000000
        }
        r = await ac.post('/ingest', json=payload)
        assert r.status_code == 200 or r.status_code == 202
        j = r.json()
        assert 'tx_id' in j
