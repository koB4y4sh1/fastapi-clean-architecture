"""
stream_chat_response_question.py

このモジュールは、チャットリクエストに対してストリーミングでAI応答を返すための関数を提供します。
"""

import os
from typing import Any, AsyncGenerator

from src.agent.chat_stream_completion_agent import chat_stream_completion_agent
from src.schema.model.chat import  Conversation


# 環境変数からAzure OpenAI設定を取得
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

async def generate_chat_message_stream(conversation: Conversation)-> AsyncGenerator[dict|str, Any]:
    """
    チャットリクエストに対してストリーミングでAI応答を返す非同期ジェネレータ。

    Args:
        chat (ChatModel): チャットの内容を含むモデル。

    Yields:
        dict: {
            "content": str,  # AIからの応答チャンク
            "index": int,   # チャンクのインデックス
            "finish_reason": str（省略される場合あり）
        }
    """
    index=0
    async for data in chat_stream_completion_agent(conversation.user_message()):
        # referenceやfollowupへの切り詰め処理はこちら
        data["index"] = index
        yield data
        index +=1
    yield "[DONE]"