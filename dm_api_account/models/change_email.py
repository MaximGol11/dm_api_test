from pydantic import BaseModel, Field, EmailStr, ConfigDict


class ChangeEmail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)