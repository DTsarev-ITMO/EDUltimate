import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import MagicMock, patch
from uuid import uuid4
from src.app import app
from src.edultimate_api.dependencies import get_current_user, get_current_admin_user, get_current_super_admin_user
from datetime import datetime, timezone
from src.common.database.models import UserRole

class MockUser:
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role
        self.name = "Test User"

mock_user = MockUser(uuid4(), "test@example.com", UserRole.USER)
mock_admin = MockUser(uuid4(), "admin@example.com", UserRole.ADMIN)
mock_super_admin = MockUser(uuid4(), "super_admin@example.com", UserRole.SUPER_ADMIN)


@pytest.fixture(autouse=True)
async def setup_dependencies():
    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_current_admin_user] = lambda: mock_admin
    app.dependency_overrides[get_current_super_admin_user] = lambda: mock_super_admin

    yield

    app.dependency_overrides.clear()


@pytest.fixture
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
class TestUserRouter:
    # --- Test REGISTER ---
    @patch("src.edultimate_api.routers.user.UserDAO.find_one_or_none")
    @patch("src.edultimate_api.routers.user.UserDAO.add")
    @patch("src.edultimate_api.routers.user.get_password_hash")
    async def test_register_user_success(self, mock_hash, mock_add, mock_find, ac: AsyncClient):
        mock_find.return_value = None
        mock_hash.return_value = "hashed_password"

        response = await ac.post("/user/register/", json={
            "name": "Ivan",
            "password": "password123",
            "email": "new@example.com"
        })

        assert response.status_code == 201
        assert response.json() == {"message": "Вы успешно зарегистрированы!"}
        mock_add.assert_called_once()


    # --- Test LOGIN ---
    @patch("src.edultimate_api.routers.user.authenticate_user")
    @patch("src.edultimate_api.routers.user.create_access_token")
    async def test_login_success(self, mock_create_token, mock_auth, ac: AsyncClient):
        mock_auth.return_value = mock_user
        mock_create_token.return_value = "fake_token"

        response = await ac.post("/user/login/", json={
            "email": "test@example.com",
            "password": "password123"
        })

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.cookies.get("user_access_token") == "fake_token"


    # --- Test GET ME ---
    async def test_get_me(self, ac: AsyncClient):
        response = await ac.get("/user/me/")

        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"


    # --- Test GET ALL USERS (Admin) ---
    @patch("src.edultimate_api.routers.user.UserDAO.find_all")
    async def test_get_all_users_as_admin(self, mock_find_all, ac: AsyncClient):
        mock_find_all.return_value = [
            {
                "id": uuid4(),
                "name": "Иван Иванов",
                "role": UserRole.ADMIN,
                "email": "admin@example.com",
                "created_at": datetime.now(timezone.utc)
            },
            {
                "id": uuid4(),
                "name": "Петр Петров",
                "role": UserRole.USER,
                "email": "user@example.com",
                "created_at": datetime.now(timezone.utc)
            }
        ]
        response = await ac.get("/user/")

        assert response.status_code == 200
        assert len(response.json()) == 2


    # --- Test UPDATE PASSWORD ---
    @patch("src.edultimate_api.routers.user.authenticate_user")
    @patch("src.edultimate_api.routers.user.UserDAO.update")
    @patch("src.edultimate_api.routers.user.get_password_hash")
    async def test_update_password(self, mock_hash, mock_update, mock_auth, ac: AsyncClient):
        mock_auth.return_value = mock_user
        mock_hash.return_value = "new_hash"
        mock_update.return_value = True

        payload = {
            "old_password": {"password": "old_pass123"},
            "new_password": {"password_1": "new_pass", "password_2": "new_pass"}
        }
        response = await ac.put("/user/update_password/", json=payload)

        assert response.status_code == 200
        assert response.json()["message"] == "Пароль успешно изменен!"


    # --- Test DELETE ME ---
    @patch("src.edultimate_api.routers.user.authenticate_user")
    @patch("src.edultimate_api.routers.user.UserDAO.delete")
    async def test_delete_me(self, mock_delete, mock_auth, ac: AsyncClient):
        mock_auth.return_value = mock_user
        mock_delete.return_value = True

        response = await ac.request("DELETE", "/user/delete_me/", json={"password": "correct_password"})

        assert response.status_code == 200
        assert "успешно удален" in response.json()["message"]

    # --- Test LOGOUT ---
    async def test_logout(self, ac: AsyncClient):
        response = await ac.post("/user/logout/")

        assert response.status_code == 200
        assert 'user_access_token=""' in response.headers["set-cookie"]