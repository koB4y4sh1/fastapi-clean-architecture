
from pydantic import BaseModel, Field
from typing import Annotated

class ChatResponse(BaseModel):
    """
    エージェントへの入力データを表現するモデル。
    question: ユーザーからの質問内容を表現します。
    
    """
    message: Annotated[str, Field(description="回答内容", examples=["こんにちは！😊 今日はどんなお手伝いをしましょうか？"])] = None