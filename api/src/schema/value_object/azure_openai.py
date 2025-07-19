import os
from pydantic import BaseModel, Field
from typing import Annotated

class AzureOpenAIObject(BaseModel):
    """
    Azure OpenAIの設定を表現するモデル。
    APIキー、エンドポイント、デプロイメント名などを持ちます。
    """
    api_key: Annotated[str, Field(description="Azure OpenAIのAPIキー")]
    endpoint: Annotated[str, Field(description="Azure OpenAIのエンドポイント")]
    deployment_name: Annotated[str, Field(description="Azure OpenAIのデプロイメント名")]

    def to_dict(self):
        """
        設定値を辞書形式で取得します。
        
        Returns:
            dict: Azure OpenAIの設定値を含む辞書。
        """
        return {
            "api_key": self.api_key,
            "endpoint": self.endpoint,
            "deployment_name": self.deployment_name
        }