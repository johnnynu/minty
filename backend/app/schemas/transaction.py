"""Transaction schemas"""

from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    """Base transaction schema"""
    account_id: int
    category_id: int | None = None
    date: date
    payee: str = Field(..., min_length=1, max_length=200)
    amount: Decimal = Field(..., decimal_places=2)
    memo: str | None = Field(None, max_length=500)
    cleared: bool = False


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction"""
    pass


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction"""
    account_id: int | None = None
    category_id: int | None = None
    date: date | None = None
    payee: str | None = Field(None, min_length=1, max_length=200)
    amount: Decimal | None = Field(None, decimal_places=2)
    memo: str | None = Field(None, max_length=500)
    cleared: bool | None = None


class TransactionResponse(TransactionBase):
    """Schema for transaction response"""
    id: int
    user_id: int

    class Config:
        from_attributes = True
