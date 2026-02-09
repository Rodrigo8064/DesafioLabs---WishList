from datetime import datetime
from typing import Annotated, Optional

from ninja import FilterLookup, FilterSchema, Schema
from pydantic import ConfigDict, EmailStr, field_validator


class UserSchema(Schema):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    def username_min_lenght(cls, v):
        if len(v) < 3:
            raise ValueError('Username deve ter pelo menos 3 caracteres')
        return v

    @field_validator('password')
    def password_min_lenght(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres')
        return v


class UserPublicSchema(Schema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime


class UserUpdateSchema(Schema):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @field_validator('username')
    def username_min_length(cls, v):
        if v is not None and len(v) < 3:
            raise ValueError('Username deve ter pelo menos 3 caracteres')
        return v

    @field_validator('password')
    def password_min_lenght(cls, v):
        if v is not None and len(v) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres')
        return v


class UserFilterSchema(FilterSchema):
    search: Annotated[
        Optional[str],
        FilterLookup(['username__icontains', 'email__icontains']),
    ] = None
