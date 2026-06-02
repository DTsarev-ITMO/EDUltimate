import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock
from uuid import uuid4
from src.app import app
from src.edultimate_api.dependencies import get_current_admin_user
from src.common.database.models import UserRole

# Используем тот же класс MockUser для имитации админа
class MockUser:
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role

mock_admin = MockUser(uuid4(), "admin@example.com", UserRole.ADMIN)

@pytest.fixture(autouse=True)
async def setup_food_dependencies():
    app.dependency_overrides[get_current_admin_user] = lambda: mock_admin
    yield
    app.dependency_overrides.clear()

@pytest.fixture
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
class TestFoodRouter:
    # --- Test GET ALL ---
    @patch("src.edultimate_api.routers.food.FoodDAO.find_all")
    async def test_get_all_foods(self, mock_find_all, ac: AsyncClient):
        mock_find_all.return_value = [
            {"name": "Apple", "protein": 0, "fats": 0, "carbs": 10, "calories": 40},
            {"name": "Banana", "protein": 0, "fats": 0, "carbs": 10, "calories": 40},
        ]
        response = await ac.get("/food/")
        assert response.status_code == 200
        assert len(response.json()) == 2


    # --- Test GET BY FILTER ---
    @patch("src.edultimate_api.routers.food.FoodDAO.find_one_or_none")
    async def test_get_food_by_filter_success(self, mock_find_one, ac: AsyncClient):
        mock_find_one.return_value = {"name": "Apple", "protein": 0, "fats": 0, "carbs": 10, "calories": 40}
        response = await ac.get("/food/by_filter", params={"name": "Apple"})
        assert response.status_code == 200
        assert response.json()["name"] == "Apple"


    async def test_get_food_by_filter_not_found(self, ac: AsyncClient):
        with patch("src.edultimate_api.routers.food.FoodDAO.find_one_or_none", return_value=None):
            response = await ac.get("/food/by_filter", params={"name": "Ghost"})
            assert response.status_code == 404


    # --- Test ADD FOOD ---
    @patch("src.edultimate_api.routers.food.FoodDAO.add")
    async def test_add_food_success(self, mock_add, ac: AsyncClient):
        mock_add.return_value = True
        payload = {"name": "Orange", "protein": 1, "fats": 0.1, "carbs": 12, "calories": 47}
        response = await ac.post("/food/add/", json=payload)
        assert response.status_code == 200
        assert response.json()["message"] == "Продукт успешно добавлен!"


    # --- Test UPDATE FOOD ---
    @patch("src.edultimate_api.routers.food.FoodDAO.update")
    async def test_update_food_success(self, mock_update, ac: AsyncClient):
        mock_update.return_value = True
        food_id = uuid4()
        payload = {"name": "Updated Apple", "calories": 60}

        response = await ac.put(f"/food/update/{food_id}", json=payload)
        assert response.status_code == 200
        assert "успешно обновлена" in response.json()["message"]


    # --- Test DELETE FOOD ---
    @patch("src.edultimate_api.routers.food.FoodDAO.delete")
    async def test_delete_food_success(self, mock_delete, ac: AsyncClient):
        mock_delete.return_value = True
        food_id = uuid4()
        response = await ac.delete(f"/food/delete/{food_id}")
        assert response.status_code == 200
        assert "удален" in response.json()["message"]