from fastapi import APIRouter
from src.urls import post_chat
from src.urls import post_chat_stream
from src.urls import post_mcp_github

api_router = APIRouter()
api_router.include_router(post_chat.router, tags=["Chat"],)
api_router.include_router(post_chat_stream.router, tags=["Chat"],)
api_router.include_router(post_mcp_github.router, tags=["MCP"],)