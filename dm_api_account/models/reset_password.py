from pydantic import BaseModel, Field, EmailStr, ConfigDict


class ResetPassword(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(...)
    email: EmailStr = Field(...)