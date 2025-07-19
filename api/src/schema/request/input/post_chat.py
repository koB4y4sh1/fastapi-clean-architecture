
from pydantic import BaseModel, Field
from typing import Annotated

class ChatRequest(BaseModel):
    message: Annotated[str, Field(description="質問内容")]
    