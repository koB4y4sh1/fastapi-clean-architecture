from src.agent.orchestrator import orchestrator
from src.repository.get_agent import get_agent
from src.repository.get_plugins import get_plugins
from src.repository.get_azure_openai_for_orchestrator import get_azure_openai_for_orchestrator
async def start_orchestrator():
    """
    オーケストレーター関数。プラグイン、オーケストレーター設定、AIモデルを受け取り、対話型エージェントを起動する。
    Args:
        data (AgentRepo): エージェントの設定情報を含む辞書。
        ai_model (AzureOpenAIRepo): Azure OpenAI などのAIモデル設定。
        plugins (PluginRepo): 利用するプラグインのリスト。
        Returns:
        None
    """
    # エージェントの設定値を取得
    agent_data = get_agent()
    # プラグインの設定値を取得
    plugins = get_plugins()
    # AIモデルの設定値を取得
    ai_model = get_azure_openai_for_orchestrator()
    # オーケストレーターを起動
    await orchestrator(agent_data, ai_model, plugins)