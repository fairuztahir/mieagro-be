import pytest
import os
from sanic_testing.testing import SanicASGITestClient


@pytest.mark.asyncio
async def test_ping_asgi_client(app):
    test_client = SanicASGITestClient(app)
    request, response = await test_client.get("/ping")

    assert request.method.lower() == "get"
    assert response.status == 200


@pytest.mark.asyncio
async def test_user_auth_unsuccessful(app):
    test_client = SanicASGITestClient(app)
    data = {
        'email': 'admin',
        'challenge': 'admin'
    }
    _, res = await test_client.post('/v1/login', json=data)

    assert res.status == 200
    assert res.json['status'] == 10010


@pytest.mark.asyncio
async def test_user_auth_successfully(app):
    test_client = SanicASGITestClient(app)
    data = {
        'email': os.getenv('API_ADMIN_EMAIL'),
        'challenge': os.getenv('API_ADMIN_PASSWORD')
    }
    _, res = await test_client.post('/v1/login', json=data)

    assert res.status == 200
    assert res.json['message'] == "Success"
    assert 'token' in res.json['data']
    assert res.json['data']['token'] is not None
