

from src.agent.invoke_mcp_tools_chat_agent import invoke_mcp_tools_chat_agent
from src.schema.model.chat import Conversation, AssistantContent

async def generate_chat_message_about_github(conversation: Conversation) -> AssistantContent:
    """
    会話履歴に対しての回答を生成する。
    Args:
        conversation (Conversation): 過去の会話含めたチャットモデル。
    Returns:
        AssistantContent: AIからの回答モデル。
    """
    # AI空の回答を受け取る
    response = await invoke_mcp_tools_chat_agent(message=conversation.user_message())
    return AssistantContent(message=response or "AIからの回答が取得できませんでした。")