from fastapi import APIRouter
from api.v1.routes.auth import accounts
from api.v1.routes.user import users
from api.v1.routes.admin import admin
from api.v1.routes.book import books

version_one = APIRouter(prefix="/api/v1")

version_one.include_router(accounts)
version_one.include_router(users)
version_one.include_router(admin)
version_one.include_router(books)
