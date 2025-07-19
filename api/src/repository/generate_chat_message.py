import os

from src.agent.chat_completion_agent import chat_completion_agent
from src.schema.model.chat import Conversation, AssistantContent

# 環境変数からAzure OpenAI設定を取得
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

async def generate_chat_message(conversation: Conversation) -> AssistantContent:
    """
    会話履歴に対しての回答を生成する。
    Args:
        conversation (Conversation): 過去の会話含めたチャットモデル。
    Returns:
        AssistantContent: AIからの回答モデル。
    """
    # AI空の回答を受け取る
    response = await chat_completion_agent(message=conversation.user_message())
    return AssistantContent(message=response or "AIからの回答が取得できませんでした。")