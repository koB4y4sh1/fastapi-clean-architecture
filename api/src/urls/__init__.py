from fastapi import APIRouter
from src.urls import post_chat

api_router = APIRouter()
api_router.include_router(post_chat.router, tags=["Agent"],)