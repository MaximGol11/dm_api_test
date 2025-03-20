from typing import Optional
from pydantic import BaseModel, Field
from dm_api_account.models.user_envelope import UserEnvelope, User


class Info(BaseModel):
    value: str
    parse_mode: str = Field(..., alias='parseMode')


class Paging(BaseModel):
    posts_per_page: int = Field(..., alias='postsPerPage')
    comments_per_page: int = Field(..., alias='commentsPerPage')
    topics_per_page: int = Field(..., alias='topicsPerPage')
    messages_per_page: int = Field(..., alias='messagesPerPage')
    entities_per_page: int = Field(..., alias='entitiesPerPage')


class Settings(BaseModel):
    color_schema: str = Field(..., alias='colorSchema')
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage')
    paging: Paging


class UserExtended(User):
    icq: Optional[str] = None
    skype: Optional[str] = None
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: str # в ответе приходит пустая строка и она не валидируется в объект Info
    settings: Settings


class UserDetailsEnvelope(UserEnvelope):
    resource: Optional[UserExtended] = None