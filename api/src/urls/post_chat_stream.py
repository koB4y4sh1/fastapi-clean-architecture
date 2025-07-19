from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.application.chat_message_stream import chat_stream
from src.schema.model.chat import ChatMessage, UserContent
from src.schema.request.input.post_chat import ChatRequest

router = APIRouter()

@router.post(
    "/chat/stream", 
    summary="入力された質問に対しての回答を生成する(ストリーム)",
    description="AIに質問を送信し、回答を受け取ります。 \n\n回答はストリーミングで受け取ります。",
    response_class=StreamingResponse,
    responses={
        200: {
            "content": {
                "text/event-stream": {
                    "example": (
                        'data: {"conetnt":"こんにちは。","index":0}\n\n'
                        'data: {"conetnt":"何をお手伝いできますか？","index":1}\n\n'
                        'data: {"conetnt":"ご質問の内容について、","index":2}\n\n'
                        'data: {"conetnt":"詳しく教えてください。","index":3,"finish_reason": {"type":"finished_answer"}}\n\n'
                        'data: [DONE]\n\n'
                    )
                }
            },
            "description": "ストリーミング形式の応答（Server-Sent Events）"
        }
    }
)
async def post_chat(
    request: ChatRequest,
):
    chat = ChatMessage(user=UserContent(**request.model_dump()))
    generator = chat_stream(chat)
    return StreamingResponse(generator, media_type="text/event-stream")