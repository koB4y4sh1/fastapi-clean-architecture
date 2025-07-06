from pydantic import BaseModel, Field

class UserId(BaseModel):
    value: int = Field(..., ge=1)

    class Config:
        frozen = True
        from_attributes = True

    def __str__(self):
        return str(self.value)