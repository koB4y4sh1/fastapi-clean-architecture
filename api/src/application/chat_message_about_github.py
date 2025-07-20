
from src.repository.generate_chat_message_about_github import generate_chat_message_about_github
from src.schema.model.chat import ChatMessage, Conversation


async def chat_message_about_github(chat_message:ChatMessage) -> ChatMessage:
    """
    """
    # 過去の会話履歴を取得
    
    # 会話履歴モデルを生成
    messages = [chat_message]
    conversation = Conversation(messages=messages)
    
    # 回答を取得
    chat_message.assistant = await generate_chat_message_about_github(conversation)

    # 会話をDBに保存する

    return chat_message