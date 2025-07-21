import os

from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments



# 環境変数からAzure OpenAI設定を取得
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

async def chat_completion_agent(message: str):
    # Kernelとサービスのセットアップ
    kernel = Kernel()
    service = AzureChatCompletion(
        api_key=AZURE_OPENAI_API_KEY,
        endpoint=AZURE_OPENAI_ENDPOINT,
        deployment_name=AZURE_OPENAI_DEPLOYMENT
    )
    kernel.add_service(service)

    # プロンプト実行設定（必要に応じて調整）
    settings = AzureChatPromptExecutionSettings(
        temperature=0.7,
        max_tokens=512,
        top_p=0.95
    )

    # ChatCompletionAgentの作成
    agent = ChatCompletionAgent(
        kernel=kernel,
        service=service,
        arguments=KernelArguments(settings),
    )

    # ユーザーの入力をAIに送信し、応答を取得
    response = None
    async for response in agent.invoke(message):
        response = response.message.content
        break  # 1回だけ取得

    return response