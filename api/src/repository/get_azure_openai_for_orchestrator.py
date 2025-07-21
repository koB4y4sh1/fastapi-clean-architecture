import os

from src.schema.value_object.azure_openai import AzureOpenAIObject

def get_azure_openai_for_orchestrator():
    """
    オーケストレーターで使用するAzureOpenAIの設定情報を取得します。
    
    Returns:
        AzureOpenAIRepo: オーケストレーターで使用するAzureOpenAIの設定情報を持つモデル。
    """
    return AzureOpenAIObject(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    )