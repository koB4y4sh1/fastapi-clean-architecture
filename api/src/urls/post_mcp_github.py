from fastapi import APIRouter, Depends

from src.application.chat_message_about_github import chat_message_about_github
from src.schema.model.chat import ChatMessage, UserContent
from src.schema.model.user import User
from src.schema.request.input.post_chat import ChatRequest
from src.schema.request.output.post_chat import ChatResponse
from src.utils.get_current_user import get_current_user

router = APIRouter()

@router.post(
    "/mcp/github", 
    summary="GitHubへの質問に対しての回答を生成する",
    description="GitHubの情報と質問内容から、AIが適した回答を生成します。 \n\n回答は文字列で受け取ります。",
    response_model=ChatResponse,
    response_description="GitHubの情報が含まれた回答内容"
)
async def post_mcp_github(
    request: ChatRequest,
    user:User = Depends(get_current_user)
):
    chat_message = ChatMessage(user=UserContent(**request.model_dump()))
    result = await chat_message_about_github(chat_message)
    return ChatResponse(**result.assistant.model_dump())