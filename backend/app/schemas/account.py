"""Account schemas"""

from decimal import Decimal
from pydantic import BaseModel, Field
from app.models.account import AccountType


class AccountBase(BaseModel):
    """Base account schema"""
    name: str = Field(..., min_length=1, max_length=100)
    type: AccountType
    balance: Decimal = Field(default=Decimal("0.00"), decimal_places=2)


class AccountCreate(AccountBase):
    """Schema for creating an account"""
    pass


class AccountUpdate(BaseModel):
    """Schema for updating an account"""
    name: str | None = Field(None, min_length=1, max_length=100)
    type: AccountType | None = None
    balance: Decimal | None = Field(None, decimal_places=2)


class AccountResponse(AccountBase):
    """Schema for account response"""
    id: int
    user_id: int

    class Config:
        from_attributes = True
