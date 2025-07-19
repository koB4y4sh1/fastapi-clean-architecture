
from pydantic import BaseModel, Field
from typing import Annotated

class ChatRequest(BaseModel):
    """
    エージェントへの入力データを表現するモデル。
    question: ユーザーからの質問内容を表現します。
    
    """

    question: Annotated[str, Field(description="質問内容")]
    