from fastapi import APIRouter
from src.adapter.api import get_users
from src.adapter.api import post_user

api_router = APIRouter()
api_router.include_router(get_users.router, tags=["users"],)
api_router.include_router(post_user.router, tags=["users"],)
