from pydantic import BaseModel, ConfigDict, Field, EmailStr

class UserCreateRequest(BaseModel):
    name: str = Field(..., title="名前", description="ユーザーのフルネーム")
    email: EmailStr = Field(..., title="メールアドレス", description="ユーザーのメールアドレス")

class UserResponse(BaseModel):
    id: int = Field(..., description="ユーザーID", example=1)
    name: str = Field(..., description="ユーザー名", example="山田 太郎")
    email: str = Field(..., description="ユーザーのメールアドレス", example="taro@example.com")

    model_config = ConfigDict(from_attributes=True)
