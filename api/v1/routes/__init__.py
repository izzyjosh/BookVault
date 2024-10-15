from fastapi import APIRouter
from api.v1.routes.auth import accounts

version_one = APIRouter(prefix="/api/v1")

version_one.include_router(accounts)
