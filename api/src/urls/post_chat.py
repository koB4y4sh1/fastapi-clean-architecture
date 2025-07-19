from fastapi import APIRouter

from src.application.chat_message import chat
from src.schema.model.chat import ChatMessage, UserContent
from src.schema.request.input.post_chat import ChatRequest
from src.schema.request.output.post_chat import ChatResponse

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
):
    chat_message = ChatMessage(user=UserContent(**request.model_dump()))
    result = await chat(chat_message)
    return ChatResponse(**result.assistant.model_dump())