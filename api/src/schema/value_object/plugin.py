from pydantic import BaseModel, Field
from typing import Literal, Optional, Annotated

class PluginObject(BaseModel):
    """
    プラグインの基本情報を表現するモデル。
    プラグイン名、タイプ、説明、パスなどを持ちます。
    """
    name: Annotated[str, Field(description="プラグイン名")]
    type: Annotated[Literal["function", "agent", "tool", "MCPStdioPlugin"], Field(description="プラグインの種別")]
    description: Annotated[Optional[str], Field(description="プラグインの説明")] = None
    path: Annotated[Optional[str], Field(description="プラグインのパス")] = None