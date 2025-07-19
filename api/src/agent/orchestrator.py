# Copyright (c) Microsoft. All rights reserved.

import asyncio

from contextlib import AsyncExitStack
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.contents import ChatHistorySummarizationReducer,FunctionCallContent, FunctionResultContent
from semantic_kernel.contents.chat_message_content import ChatMessageContent

from src.schema.value_object.agent import AgentObject
from src.schema.value_object.azure_openai import AzureOpenAIObject
from src.schema.value_object.plugin import PluginObject
from src.mcp_plugin.create_mcp_pugins import create_mcp_pugins

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

async def orchestrator(agent_data:AgentObject, ai_model:AzureOpenAIObject, plugins:list[PluginObject]):
    """
    オーケストレーター関数。プラグイン、オーケストレーター設定、AIモデルを受け取り、対話型エージェントを起動する。

    Args:
        settings (AgentObject): エージェントの設定情報を含む辞書。
        ai_model (AzureOpenAIObject): Azure OpenAI などのAIモデル設定。
        plugins (PluginObject): 利用するプラグインのリスト。

    Returns:
        None

    Note:
        - 対話履歴の要約やプラグインの初期化、エージェントの作成、ユーザー入力の受付と応答を行う。
        - "exit" と入力することで対話を終了できる。
    """
    REDUCER_MSG_COUNT = 1      # 要約を適用した後に保持するメッセージの目標数
    REDUCER_THRESHOLD = 0      # 現在のメッセージ数がtarget_countを超過したときに、履歴が早期に削減されるのを防ぐためのバッファ
    AUTO_MESSAGE_SUMMARIZATION = True  # add_message_asuyncを使用して新規メッセージを追加した後、チャット履歴を自動的に要約するかどうか

    service_id = "orchestrator"
    
    # カーネル作成
    kernel = Kernel()

    # Kernelにサービスを登録
    kernel.add_service(AzureChatCompletion(service_id=service_id))

    # AzureChatCompletionの設定
    # settings = AzureChatPromptExecutionSettings(**agent_data.model.options.model_dict())
    settings = AzureChatPromptExecutionSettings(
        temperature=agent_data.model.options.temperature,
        max_tokens=agent_data.model.options.max_tokens,
        top_p=agent_data.model.options.top_p,
        response_format=agent_data.model.options.response_format,
    )

    # 要約リデューサーを作成
    history_summarization_reducer = ChatHistorySummarizationReducer(
        service=AzureChatCompletion(), 
        target_count=REDUCER_MSG_COUNT, 
        threshold_count=REDUCER_THRESHOLD,
        auto_reduce=AUTO_MESSAGE_SUMMARIZATION,
        use_single_summary=False,
        include_function_content_in_summary=True,
    )
    
    # 前回までの会話の要約を追加
    history_summarization_reducer.add_assistant_message("ユーザーは日本語で挨拶し、AIの能力について尋ねた後、観光地に関する詳細を求めました。AIはユーザーの希望する観光地に沿った情報提供を提案しました。ユーザーは具体的に日本の京都について知りたいとリクエストしました。")
    
    # MCPプラグイン(stdio transport)を作成
    mcp_plugins = await create_mcp_pugins(
        plugins, ai_model
    )
    
    async with AsyncExitStack() as stack:
        # MCPプラグインをコンテキストマネージャとして登録
        agent_instances = []
        for mcp_plugin in mcp_plugins:
            instance = await stack.enter_async_context(mcp_plugin)
            agent_instances.append(instance)

        # プラグインをカーネルに追加
        kernel.add_plugins(agent_instances)
        
        

        # エージェントを作成（create_from_dictではmodel.options.settingsにAzureChatPromptExecutionSettingsの情報を渡す必要がある）
        # agent: ChatCompletionAgent = await AgentRegistry.create_from_dict(
        #         agent_data.to_dict(), kernel=kernel, service=AzureChatCompletion(
        #             api_key=ai_model.api_key, 
        #             endpoint=ai_model.endpoint, 
        #             deployment_name=ai_model.deployment_name
        #         ),
        # )

        # エージェントを作成（）
        agent = ChatCompletionAgent(
            kernel=kernel,
            service=AzureChatCompletion(
                api_key=ai_model.api_key,
                endpoint=ai_model.endpoint,
                deployment_name=ai_model.deployment_name
            ),
            arguments=KernelArguments(settings),
        )

        # 2. 会話を保持するスレッドを作成
        # スレッドが指定されていない場合は新しく作成され、
        # 最初の応答とともに返されます
        thread: ChatHistoryAgentThread = ChatHistoryAgentThread(chat_history=history_summarization_reducer)
        while True:
            user_input = input("User: ")
            if user_input.lower() == "exit":
                break
            # 3. Invoke the agent for a response
            async for response in agent.invoke(messages=user_input, thread=thread, on_intermediate_message=handle_intermediate_steps):
            # デバッグ用に内容を出力
                print(f"Response content:\n{response.message.content}")
                # try:
                #     # JSON フォーマットを検証
                #     reasoned_result = StructuredResult.model_validate(json.loads(response.message.content))
                #     print(f"# {response.name}:\n\n{reasoned_result.model_dump_json(indent=4)}")
                # except json.JSONDecodeError as e:
                #     print(f"JSONDecodeError: {e}")
                #     print("Response content is not valid JSON.")
                thread = response.thread

            # Attempt reduction
            # target_countは0にできず、そのままではAIの回答を要約に含めることはできない
            is_reduced = await thread.reduce()
            print(f"@ Message Count: {len(thread)}\n")
            if is_reduced:
                print(f"@ History reduced to {len(thread)} messages.")
                    # If reduced, print summary if present    
                async for msg in thread.get_messages():
                    if msg.metadata and msg.metadata.get("__summary__"):
                        print(f"\tSummary: {msg.content}")
                        break

        # 4. Cleanup: スレッドを削除
        await thread.delete() if thread else None
    


"""
User: あなたができることを教えてください。
# PersonalAssistant: 私はレストランの予約やメニューに関する質問への回答、計算のサポート、および現在の日時に関連する情報の提供が可能です。
User: どのようなレストランありますか？
# PersonalAssistant: 利用可能なレストランには次のものがあります：AAA（田舎風の雰囲気が特徴のステーキハウス）、BBB（海の景色を楽しめる魚料理を中心としたレストラン）、およびCCC（多様なメニューを提供するカジュアルな飲食店）。"
User: レストランAAAは素敵ですね、スペシャルメニューを教えてください。
# PersonalAssistant:  "'AAA'の特別メニューについてお知らせします：\n\n- **特製エントリー**: Tボーンステーキ\n- **特製サラダ**: シーザーサラダ\n- **特製ドリンク**: オールドファッションド\n\nこれらはRusticな雰囲気を楽しみながら新鮮で美味しい料理を味わう理想的な選択肢です。さらに詳細についてご希望でしたらお知らせください。"
User: Tボーンステーキ は美味しそう　値段いくらですか
# PersonalAssistant: レストランAAAのTボーンステーキの値段は$9.99です。美味しそうですね！予約や他のメニューについて知りたいことがあれば教えてください。
User: オールドファッションの値段は？
# PersonalAssistant: レストランAAAのオールドファッションの値段は$9.99です。お飲み物も楽しめそうですね！他に知りたいことがあれば教えてください。
User: Tボーンステーキとオールドファッションを3人分頼みたい　合計金額いくらいですか  
# PersonalAssistant: 3人分のTボーンステーキ($9.99)とオールドファッション($9.99)を注文した場合の合計金額は、**$59.94**です。ご注文を検討されますか？または予約のお手伝いが必要ですか？
User: それで明日の20時に予約でお願いします。
# PersonalAssistant: レストランAAAで明日の20時に予約が確定しました。楽しんでください！他にお手伝いできることがあれば教えてください。
User: ありがとう
# PersonalAssistant: どういたしまして！素敵な時間をお過ごしください。また何かお手伝いが必要なときはいつでもお声がけくださいね。😊
User: exit
"""

if __name__ == "__main__":
    asyncio.run(orchestrator())
