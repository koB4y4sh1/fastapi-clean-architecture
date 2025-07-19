from fastapi import APIRouter
from src.urls import post_chat
from src.urls import post_chat_stream

api_router = APIRouter()
api_router.include_router(post_chat.router, tags=["Agent"],)
api_router.include_router(post_chat_stream.router, tags=["Agent"],)