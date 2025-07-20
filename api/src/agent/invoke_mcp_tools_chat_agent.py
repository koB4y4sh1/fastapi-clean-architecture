
from semantic_kernel.agents import ChatHistoryAgentThread
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents import FunctionCallContent, FunctionResultContent
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings

from src.mcp_plugin.create_mcp_github_plugin import create_mcp_time_plugin
from src.schema.agent.agent import AgentWithPlugin
from src.utils.check_tools_in_mcp import check_tools_in_mcp
# コールバック関数
async def handle_intermediate_steps(message: ChatMessageContent) -> None:
    """
    このコールバック関数は、中間メッセージごとに呼び出されます。
    これにより、FunctionCallContentやFunctionResultContentを個別に処理できます。
    コールバックが指定されていない場合、エージェントは中間的なツール呼び出しステップなしで最終応答のみを返します。

    Args:
        message (ChatMessageContent): 中間メッセージコンテンツ
    
    Returns:
        None
        
    Example:
        >>> message = ChatMessageContent(role="user", content="What can you do?")
        >>> await handle_intermediate_steps(message)
    
    Note:
        - FunctionCallContentは、関数呼び出しの詳細を含むメッセージです。
        - FunctionResultContentは、関数呼び出しの結果を含むメッセージです。
    """
    for item in message.items or []:
        if isinstance(item, FunctionCallContent):
            print(f"Function Call:> {item.name} with arguments: {item.arguments}")
        elif isinstance(item, FunctionResultContent):
            print(f"Function Result:> {item.result} for function: {item.name}")
        else:
            print(f"{message.role}: {message.content}")


async def invoke_mcp_tools_chat_agent(message:str) -> ChatMessageContent:
    """エージェントを使用してMCPツールを呼び出す"""
    # プラグインの作成
    time_plugin = create_mcp_time_plugin()

    async with time_plugin:

        # 利用可能なツール一覧を取得
        await check_tools_in_mcp(time_plugin)

        # エージェントの作成
        agent = AgentWithPlugin(
            settings=AzureChatPromptExecutionSettings(),
            name="github-chat-agent",
            instructions="You are helpful assistant.",
            plugins=[time_plugin]
        ).create_agent()

        # 会話履歴管理スレッドの作成
        thread: ChatHistoryAgentThread = None

        async for response in agent.invoke(messages=message, thread=thread,  on_intermediate_message=handle_intermediate_steps):
            content = response.message.content
            thread = response.thread
            print(f"{response.role}: {content}")
            break  # 1回だけ取得

        # Cleanup: スレッドの削除
        await thread.delete() if thread else None

        return content