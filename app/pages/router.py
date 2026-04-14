from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.food.router import get_all_foods


router = APIRouter(prefix='/pages', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/templates')


@router.get('/food')
async def get_food_html(request: Request, foods = Depends(get_all_foods)):
    return templates.TemplateResponse(request=request, name='food.html', context={'foods': foods})