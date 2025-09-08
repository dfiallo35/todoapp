from pydantic import BaseModel
from datetime import datetime
from pydantic import field_validator


class BaseEntity(BaseModel):
    id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("id", mode="before")
    def validate_id(cls, data):
        if data:
            return str(data)
        return data


class BaseUpdateSchema(BaseModel):
    pass


class Task(BaseEntity):
    title: str
    description: str | None = None

    user_id: str

    @field_validator("user_id", mode="before")
    def validate_user_id(cls, data):
        if data:
            return str(data)
        return data


class TaskUpdateSchema(BaseUpdateSchema):
    title: str | None = None
    description: str | None = None


class User(BaseEntity):
    username: str
    hashed_password: str


class UserSignup(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
