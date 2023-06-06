from pydantic import BaseModel, Field
from beanie import Document, Indexed
from typing import Optional
from datetime import datetime


class User(Document):
    username: Indexed(str)
    password: str
    incorrect_password_attempts: Optional[int] = 0
    created_at: datetime = datetime.now()
    lockout_timestamp: Optional[datetime]

    class Settings:
        name = "user"


class UserRequest(BaseModel):
    username: str = Field(..., description='Desired username for the account, with a minimum length of 3 characters and a maximum length of 32 characters')
    password: str = Field(..., description='''Password for the account, with a minimum length of 8 characters and a maximum length of 32 characters
    containing at least 1 uppercase letter, 1 lowercase letter, and 1 number.''')

    class Config:
        schema_extra = {
            "example": {
                "username": "testuser",
                "password": "Password1",
            }
        }
        extra = "forbid"


class UserResponse(BaseModel):
    success: bool = Field(..., description='Indicates the result of the account creation process.')
    reason: Optional[str] = Field(..., description='Specifies the reason for a failed account creation process.')

    class Config:
        schema_extra = {
            "example": {
                "success": True,
            }
        }
