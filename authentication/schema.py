from ninja import Schema
from pydantic import field_validator


class LoginSchema(Schema):
    username: str
    password: str

    @field_validator('password')
    def password_min_length(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres')
        return v


class Token(Schema):
    access_token: str
    token_type: str


class ErrorSchema(Schema):
    error: str
