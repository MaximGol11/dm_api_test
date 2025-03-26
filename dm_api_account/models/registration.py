from pydantic import BaseModel, Field, ConfigDict


class Registration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: str = Field(...)
    password: str = Field(...)
    email: str = Field(...) # Иначе возмжоно передать только валидный email в тесте.