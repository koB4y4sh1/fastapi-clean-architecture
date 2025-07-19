from datetime import datetime, UTC

from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Annotated

class UserContent(BaseModel):
    id: Annotated[UUID, Field(description="メッセージID")] = uuid4()
    message: Annotated[str, Field(description="ユーザーの質問")]
    images: Annotated[list[str]| None, Field(description="添付画像")] = None
    files: Annotated[list[str]| None, Field(description="添付ファイル")]  = None

class AssistantContent(BaseModel):
    id: Annotated[UUID, Field(description="メッセージID")] = uuid4()
    message: Annotated[str, Field(description="アシスタントの回答")] = ""
    reference: Annotated[list[str]| None, Field(description="回答の引用資料") ] = None
    followup: Annotated[list[str]| None, Field(description="質問のフォローアップ") ] = None

class ChatMessage(BaseModel):
    """
    単一の会話のやりとりを表すモデル。
    """
    history_no: Annotated[int, Field(description="会話履歴番号")] = 0
    user: Annotated[UserContent, Field(description="ユーザーの入力内容")]
    assistant: Annotated[AssistantContent, Field(description="アシスタントの回答内容")] = AssistantContent()
    timestamp: Annotated[datetime, Field(description="送信日時(UTC)")] = datetime.now(UTC)


class Conversation(BaseModel):
    """
    一連の会話履歴をまとめるモデル。
    messages は時系列順で並ぶ。
    """
    session_id: Annotated[str, Field(description="セッションID")] = "0"
    messages: Annotated[list[ChatMessage], Field(description="メッセージ履歴")] = []

    def user_message(self)->str:
        return self.messages[0].user.message