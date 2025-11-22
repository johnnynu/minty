"""User schemas"""

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user"""
    clerk_user_id: str


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    clerk_user_id: str
    created_at: datetime

    class Config:
        from_attributes = True
