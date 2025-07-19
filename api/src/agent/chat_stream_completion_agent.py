
import os
from typing import Any, AsyncGenerator

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments


# 環境変数からAzure OpenAI設定を取得
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

"""
chat_stream_completion_agent.py

このモジュールは、Azure OpenAIのストリーミングチャット応答から生チャンク（str）のみを返す関数を提供します。
"""
def _build_kernel():
    kernel = Kernel()
    service = AzureChatCompletion(
        api_key=AZURE_OPENAI_API_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT,
        deployment_name=AZURE_OPENAI_DEPLOYMENT,
    )
    kernel.add_service(service)
    return kernel, service

async def chat_stream_completion_agent(messages: str) -> AsyncGenerator[dict, Any]:
    """
    Azure OpenAIのストリーミングチャット応答から、各チャンクの内容（content）および必要に応じてfinish_reasonを含むdictをストリームで返す非同期ジェネレータ。
    OpenAIレスポンス構造やSSE形式には依存しません。

    Args:
        messages (str): ユーザーからの入力メッセージ。

    Yields:
        dict: {
            "content": str,  # AIからの応答チャンク
            "finish_reason": str（省略される場合あり）
        }
    """
    kernel, service = _build_kernel()
    settings = AzureChatPromptExecutionSettings(
        temperature=0.7,
        max_tokens=512,
        top_p=0.95,
        stream=True,
    )
    agent = ChatCompletionAgent(
        kernel=kernel,
        service=service,
        arguments=KernelArguments(settings),
    )
    async for response in agent.invoke_stream(messages=messages):
        chunk = response.message.content
        if not chunk:
            continue
        data = {
            "content": response.message.content
        }
        if response.message.finish_reason is not None:
            data["finish_reason"] = response.message.finish_reason
        yield data