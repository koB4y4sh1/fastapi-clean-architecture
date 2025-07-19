from src.repository.generate_chat_message import generate_chat_message
from src.schema.model.chat import ChatMessage, Conversation


async def chat(chat_message:ChatMessage) -> ChatMessage:
    """
    """
    # 過去の会話履歴を取得
    
    # 会話履歴モデルを生成
    messages = [chat_message]
    conversation = Conversation(messages=messages)
    
    # 回答を取得
    chat_message.assistant = await generate_chat_message(conversation)

    # 会話をDBに保存する

    return chat_message