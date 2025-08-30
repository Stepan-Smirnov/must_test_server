from fastapi import APIRouter

from app.api.endpoints import data_router

main_router = APIRouter(prefix="/api")

main_router.include_router(
    router=data_router,
    prefix="/data",
    tags=["Блок с данными"],
)
