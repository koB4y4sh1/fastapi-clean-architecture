
from src.schema.model.chat import ChatModel

async def chat(chat: ChatModel) -> ChatModel:
    """
    AIに質問送信し、回答を返却する
    Args:
        chat (ChatModel): チャットの内容を含むモデル。
    Returns:
        ChatModel: AIからの回答を含むモデル。
    """
    chat.answer = "AIからの回答"

    return chat