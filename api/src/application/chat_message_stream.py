
import json
from typing import Any, AsyncGenerator

from src.repository.generate_chat_message_stream import generate_chat_message_stream
from src.schema.model.chat import ChatMessage, Conversation
# from src.repository.save_conversation import save_conversation  # 仮のDB保存リポジトリ

async def chat_stream(chat_message: ChatMessage) -> AsyncGenerator[str,Any]:
    """
    チャットメッセージをストリーミングで返し、全チャンク送信後にDBへ保存する。

    Args:
        chat_message (ChatMessage): ユーザーからのチャットメッセージ。

    Yields:
        str: SSE形式のAI応答チャンク（JSON文字列）。
            例: 'data: {"content": "こんにちは。", "index": 0}\n\n'
            finish_reasonがある場合は含まれる。
    """
    # 会話履歴モデルを生成
    messages = [chat_message]
    conversation = Conversation(messages=messages)
    
    # ストリーム応答を生成
    assistant_content = ""
    async for data in generate_chat_message_stream(conversation):
        if isinstance(data,dict):
            assistant_content += data.get("content","")
            yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
        else:
            yield f"data: {data}\n\n"
    
    # 全チャンク送信後にDB保存
    chat_message.assistant.message = assistant_content
    # save_conversation(chat_message)