"""Budget allocation schemas"""

from decimal import Decimal
from pydantic import BaseModel, Field, field_validator
import re


class BudgetAllocationBase(BaseModel):
    """Base budget allocation schema"""
    category_id: int
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$")
    amount: Decimal = Field(..., decimal_places=2)

    @field_validator("month")
    @classmethod
    def validate_month_format(cls, v: str) -> str:
        """Validate month is in YYYY-MM format"""
        if not re.match(r"^\d{4}-(0[1-9]|1[0-2])$", v):
            raise ValueError("Month must be in YYYY-MM format with valid month (01-12)")
        return v


class BudgetAllocationCreate(BudgetAllocationBase):
    """Schema for creating a budget allocation"""
    pass


class BudgetAllocationUpdate(BaseModel):
    """Schema for updating a budget allocation"""
    amount: Decimal = Field(..., decimal_places=2)


class BudgetAllocationResponse(BudgetAllocationBase):
    """Schema for budget allocation response"""
    id: int
    user_id: int

    class Config:
        from_attributes = True
