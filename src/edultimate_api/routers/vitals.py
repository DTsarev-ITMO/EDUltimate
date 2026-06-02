from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends, Response, Query
from src.common.database.dao import VitalDAO
from src.common.database.schemas.vitals_schemas import ResponseVitalGet, RequestVitalCreate
from src.edultimate_api.auth import get_password_hash, authenticate_user, create_access_token
from src.edultimate_api.dependencies import get_current_user, get_current_admin_user, get_current_super_admin_user
from src.common.database.models import User, UserVital


router = APIRouter(prefix='/vitals', tags=['Работа с жизненными показателями'])


@router.get("/", summary="Получить последнюю запись")
async def get_last_vitals(current_user: User = Depends(get_current_user)) -> ResponseVitalGet:
    vital = await VitalDAO.find_by_filter_latest(user_id=current_user.id)
    if not vital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Записи отсутствуют.')
    return vital


@router.get("/all", summary="Получить все записи")
async def get_all_vitals(current_user: User = Depends(get_current_user)) -> list[ResponseVitalGet]:
    vitals = await VitalDAO.find_by_filter(user_id=current_user.id)
    if not vitals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Записи отсутствуют.')
    return vitals.order_by(UserVital.created_at.desc())


@router.get("/{vital_id}", summary="Получить запись по id")
async def get_vital_by_id(
        vital_id: UUID,
        current_user: User = Depends(get_current_user)) -> ResponseVitalGet:
    vital = await VitalDAO.find_by_filter(id=vital_id)
    if not vital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Записи отсутствуют.')
    if vital.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав! Просматривать можно лишь собственные записи.'
        )
    return vital


@router.post("/create/")
async def create_vitals(
        vitals: RequestVitalCreate,
        current_user: User = Depends(get_current_user)
) -> dict:
    check = await VitalDAO.add(**vitals.model_dump(), user_id=current_user.id)
    if check:
        return {"message": "Данные сохранены!"}
    else:
        return {"message": "Ошибка при сохранении данных!"}


@router.put("/update/{vital_id}")
async def update_vital(
        vital_id: UUID,
        vitals: RequestVitalCreate,
        current_user: User = Depends(get_current_user)
) -> dict:
    current_vitals = await VitalDAO.find_one_or_none(id=vital_id)

    if not current_vitals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись не найдена"
        )

    if current_vitals.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав! Редактировать можно лишь собственные записи.'
        )

    check = await VitalDAO.update(filter_by={'id': vital_id}, **vitals.model_dump(exclude_none=True))
    if check:
        return {"message": "Запись успешно обновлена!", "vitals": vitals}
    else:
        return {"message": "Ошибка при обновлении записи!"}


@router.delete("/delete/{vital_id}")
async def delete_vital(
        vital_id: UUID,
        current_user: User = Depends(get_current_user)
) -> dict:
    current_vitals = await VitalDAO.find_one_or_none(id=vital_id)
    if current_vitals.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Недостаточно прав! Удалить можно лишь собственные записи.'
        )
    check = await VitalDAO.delete(id=vital_id)
    if check:
        return {"message": f"Запись удалена!"}
    else:
        return {"message": "Ошибка при удалении записи!"}