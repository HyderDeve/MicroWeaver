from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class AccountBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)

class AccountCreate(AccountBase):
    password: str = Field(..., min_length=8, max_length=100)

class Account(AccountBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True