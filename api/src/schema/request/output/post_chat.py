
from pydantic import BaseModel, Field
from typing import Annotated

class ChatResponse(BaseModel):
    """
    エージェントへの入力データを表現するモデル。
    question: ユーザーからの質問内容を表現します。
    
    """

    question: Annotated[str, Field(description="質問内容")]
    answer: Annotated[str, Field(description="回答内容")] = None