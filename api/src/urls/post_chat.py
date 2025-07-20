from fastapi import APIRouter, Depends

from src.application.chat_message import chat
from src.schema.model.chat import ChatMessage, UserContent
from src.schema.model.user import User
from src.schema.request.input.post_chat import ChatRequest
from src.schema.request.output.post_chat import ChatResponse
from src.utils.get_current_user import get_current_user

router = APIRouter()

@router.post(
    "/chat", 
    summary="入力された質問に対しての回答を生成する",
    description="AIに質問を送信し、回答を受け取ります。 \n\n回答は文字列で受け取ります。",
    response_model=ChatResponse,
    response_description="回答内容"
)
async def post_chat(
    request: ChatRequest,
    user: User = Depends(get_current_user)
):
    print(user.user_principal_name)
    chat_message = ChatMessage(user=UserContent(**request.model_dump()))
    result = await chat(chat_message)
    return ChatResponse(**result.assistant.model_dump())