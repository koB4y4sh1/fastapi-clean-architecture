from pydantic import BaseModel, Field
from typing import Annotated
from src.schema.value_object.agent import AgentObject
from src.schema.value_object.azure_openai import AzureOpenAIObject
from src.schema.value_object.plugin import PluginObject

class OrchestratorParameter(BaseModel):
    """
    オーケストレーターの設定を表現するモデル。
    エージェント、プラグイン、AIモデルの設定を含みます。
    """

    agent: Annotated[AgentObject, Field(description="エージェントの設定")]
    plugins: Annotated[list[PluginObject], Field(description="プラグインの設定")]
    azure_openai: Annotated[AzureOpenAIObject, Field(description="Azure OpenAIの設定")]