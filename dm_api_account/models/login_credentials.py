from pydantic import BaseModel, Field, ConfigDict


class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(...)
    password: str = Field(...)
    remember_me: bool = Field(..., serialization_alias="rememberMe")