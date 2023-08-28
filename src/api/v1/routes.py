from fastapi import APIRouter

from .endpoints import todo, image

api_router = APIRouter()

# fmt: off
# api_router.include_router(todo.router, prefix='/todo', tags=['Todos'])
api_router.include_router(image.router, prefix='/image', tags=['Images'])