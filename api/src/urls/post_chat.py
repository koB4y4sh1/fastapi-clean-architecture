from fastapi import APIRouter
from src.application import question_to_ai
from src.application.start_orcestrator import start_orchestrator
from src.schema.model.chat import ChatModel
from src.schema.request.input.post_chat import ChatRequest
from src.schema.request.output.post_chat import ChatResponse

router = APIRouter()

@router.post(
    "/chat", 
    response_model=ChatResponse,
    summary="AIへの質問送信",
    description="AIに質問を送信し、回答を受け取ります。 \n\n質問内容はChatRequestモデルで指定します。",
)
async def post_chat(
    request: ChatRequest,
):
    await start_orchestrator()
    chat = ChatModel(**request.model_dump())
    chat = await question_to_ai.chat(chat)
    return ChatResponse(**chat.model_dump())