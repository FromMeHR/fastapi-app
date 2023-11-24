from unittest import IsolatedAsyncioTestCase
from httpx import AsyncClient
from app.main import app as web_app

class APITestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = AsyncClient(app=web_app, base_url="http://testserver")

    async def asyncTearDown(self):
        await self.client.aclose()

    async def test_main_url(self):
        response = await self.client.get("/")
        print(f"Response: {response}")
        self.assertEqual(response.status_code, 200)

    async def test_create_user(self):
        user_data = {
            'user': {
                'email': 'test124@test.com',
                'password': 'test',
                'first_name': 'Max',
                'last_name': 'Me'
            }
        }
        response = await self.client.post('/create_user', json=user_data)
        print(f"Response: {response}")
        self.assertEqual(response.status_code, 200)


