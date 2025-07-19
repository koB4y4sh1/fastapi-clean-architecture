import os
from pathlib import Path

from semantic_kernel.connectors.mcp import MCPStdioPlugin

from src.schema.value_object.plugin import PluginObject
from src.schema.value_object.azure_openai import AzureOpenAIObject

async def create_mcp_pugins(plugins:list[PluginObject], model: AzureOpenAIObject) -> list[MCPStdioPlugin]:
    """
    Pliginの情報からMCPStdioPluginインスタンスを生成する。

    Args:
        plugin_yaml_str (list[PluginObject]): YAML形式のプラグイン定義文字列。
        azure_openai_repo (AzureOpenAIObject): Azure OpenAIの設定情報を持つモデル。
    
    Returns:
        list(MCPStdioPlugin): MCPStdioPluginインスタンスのリスト。
    """
    agents = [] # エージェントのリスト
    servers_dir = Path(os.path.dirname(__file__)).parent.parent.joinpath('servers/worker').as_posix()
    
    for plugin in plugins:
        if plugin.type == "MCPStdioPlugin":
            agent = MCPStdioPlugin(
                name=plugin.name,
                description=plugin.description,
                command="uv",
                args=[
                    f"--directory={servers_dir}",
                    "run",
                    plugin.path,
                ],
                env={
                    "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME": model.deployment_name,
                    "AZURE_OPENAI_ENDPOINT": model.endpoint,
                    "AZURE_OPENAI_API_KEY": model.api_key,
                },
            )
            agents.append(agent)
        else:
            print(f"Unsupported plugin type: {plugin['type']} for plugin {plugin['name']}")
    return agents

    