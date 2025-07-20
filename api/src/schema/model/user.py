from typing import Annotated
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    name: Annotated[str, Field(description="ユーザー名")]
    email: Annotated[EmailStr, Field(description="メールアドレス")]
    user_principal_name: Annotated[EmailStr, Field(description="UPN")]