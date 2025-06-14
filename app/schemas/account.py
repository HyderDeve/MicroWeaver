from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class AccountBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = Field(None, max_length=100)

class AccountCreate(AccountBase):
    password: str = Field(..., min_length=8, max_length=100)

class Account(AccountBase):
    id: uuid.UUID 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True