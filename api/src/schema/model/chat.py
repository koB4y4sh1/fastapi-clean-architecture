from pydantic import BaseModel, Field
from typing import Annotated, Optional

class ChatModel(BaseModel):
    """
    チャットの内容を表現するモデル。
    question: ユーザーからの質問内容を表現します。
    answer: エージェントからの回答内容を表現します。
    """
    question: Annotated[str, Field(description="質問内容")]
    answer: Annotated[str, Field(description="回答内容")] = None