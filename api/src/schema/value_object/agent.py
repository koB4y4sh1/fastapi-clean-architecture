
from typing import Literal, Annotated, Any

from pydantic import BaseModel, Field
from semantic_kernel.connectors.ai.open_ai import AzureChatPromptExecutionSettings

class Options(BaseModel):
    temperature: Annotated[float, Field(description="温度パラメータ")] = 0.7
    max_tokens: Annotated[int, Field(description="最大トークン数")] = 1000
    top_p: Annotated[float, Field(description="トップPパラメータ")] = 0.9
    stream: Annotated[bool, Field(False, description="ストリーミング出力の有無")] = False
    response_format: Annotated[Any, Field(description="レスポンスフォーマット")] = None
    
class Model(Options):
    options: Annotated[Options, Field(description="カーネルのサービス設定")] = Options()

class AgentObject(Model):
    type: Annotated[Literal["chat_completion_agent"], Field(description="エージェントの種別")]
    name: Annotated[str, Field(description="エージェント名")]
    description: Annotated[str, Field(description="エージェントの説明")] = ""
    instructions: Annotated[str, Field(description="エージェントへの指示文")] = "Help the user with restaurant bookings, answer in Japanese."
    model: Annotated[Model, Field(description="エージェントのモデル設定")] = Model()

    def to_dict(self):
        """
        エージェントの設定値をdictに変換します。
        response_formatはBaseModelのままにする必要があるため、model.options.response_formatを上書きしています。

        """
        # model.options.response_format以外をdictに変更
        agent_dict = self.model_dump()  # v2系
        # model.options.settingsを設定
        agent_dict['model']['options']["settings"] = AzureChatPromptExecutionSettings(**self.model.options.model_dump())
        return agent_dict

        