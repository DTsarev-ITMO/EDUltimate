import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock
from uuid import uuid4
from src.app import app
from src.edultimate_api.dependencies import get_current_user
from src.common.database.models import UserRole


class MockUser:
    def __init__(self, id, email, role):
        self.id = id
        self.email = email
        self.role = role


my_user_id = uuid4()
mock_user = MockUser(my_user_id, "user@example.com", UserRole.USER)


@pytest.fixture(autouse=True)
async def setup_vitals_dependencies():
    app.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
class TestVitalsRouter:
    # --- GET LATEST ---
    @patch("src.edultimate_api.routers.vitals.VitalDAO.find_by_filter_latest")
    async def test_get_last_vitals(self, mock_latest, ac: AsyncClient):
        mock_latest.return_value = {"name": "name", "weight": 70.5, "LBS": 60, "fat_percentage": 14.8}
        response = await ac.get("/vitals/")
        assert response.status_code == 200


    # --- GET ALL ---
    @patch("src.edultimate_api.routers.vitals.VitalDAO.find_by_filter")
    async def test_get_all_vitals(self, mock_find, ac: AsyncClient):
        # Имитируем возвращаемый объект, у которого можно вызвать .order_by
        mock_query = MagicMock()
        mock_query.order_by.return_value = [{"name": "name", "weight": 70.5, "LBS": 60, "fat_percentage": 14.8}]
        mock_find.return_value = mock_query

        response = await ac.get("/vitals/all")
        assert response.status_code == 200


    # --- CREATE ---
    @patch("src.edultimate_api.routers.vitals.VitalDAO.add")
    async def test_create_vitals(self, mock_add, ac: AsyncClient):
        mock_add.return_value = True
        payload = {"name": "name", "weight": 70.5, "LBS": 60, "fat_percentage": 14.8}
        response = await ac.post("/vitals/create/", json=payload)
        assert response.status_code == 200


    # --- UPDATE (с проверкой владения) ---
    @patch("src.edultimate_api.routers.vitals.VitalDAO.find_one_or_none")
    @patch("src.edultimate_api.routers.vitals.VitalDAO.update")
    async def test_update_vital_success(self, mock_update, mock_find, ac: AsyncClient):
        vital_id = uuid4()
        mock_find.return_value = MagicMock(user_id=my_user_id)
        mock_update.return_value = True

        payload = {"weight": 75.0, "height": 180.0, "activity_level": 1.5}
        response = await ac.put(f"/vitals/update/{vital_id}", json=payload)
        assert response.status_code == 200
        assert "успешно обновлена" in response.json()["message"]


    # --- DELETE ---
    @patch("src.edultimate_api.routers.vitals.VitalDAO.find_one_or_none")
    @patch("src.edultimate_api.routers.vitals.VitalDAO.delete")
    async def test_delete_vital_success(self, mock_delete, mock_find, ac: AsyncClient):
        vital_id = uuid4()
        mock_find.return_value = MagicMock(user_id=my_user_id)
        mock_delete.return_value = True

        # Теперь просто DELETE без тела
        response = await ac.delete(f"/vitals/delete/{vital_id}")

        assert response.status_code == 200
        assert response.json()["message"] == "Запись удалена!"

    # --- FORBIDDEN DELETE ---
    @patch("src.edultimate_api.routers.vitals.VitalDAO.find_one_or_none")
    async def test_delete_vital_forbidden(self, mock_find, ac: AsyncClient):
        vital_id = uuid4()
        mock_find.return_value = MagicMock(user_id=uuid4())

        response = await ac.delete(f"/vitals/delete/{vital_id}")
        assert response.status_code == 403
        assert "Недостаточно прав" in response.json()["detail"]
