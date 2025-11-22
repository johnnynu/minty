"""Category schemas"""

from pydantic import BaseModel, Field


class CategoryGroupBase(BaseModel):
    """Base category group schema"""
    name: str = Field(..., min_length=1, max_length=100)
    sort_order: int = Field(default=0, ge=0)


class CategoryGroupCreate(CategoryGroupBase):
    """Schema for creating a category group"""
    pass


class CategoryGroupUpdate(BaseModel):
    """Schema for updating a category group"""
    name: str | None = Field(None, min_length=1, max_length=100)
    sort_order: int | None = Field(None, ge=0)


class CategoryGroupResponse(CategoryGroupBase):
    """Schema for category group response"""
    id: int
    user_id: int

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    """Base category schema"""
    name: str = Field(..., min_length=1, max_length=100)
    category_group_id: int
    sort_order: int = Field(default=0, ge=0)


class CategoryCreate(CategoryBase):
    """Schema for creating a category"""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category"""
    name: str | None = Field(None, min_length=1, max_length=100)
    category_group_id: int | None = None
    sort_order: int | None = Field(None, ge=0)


class CategoryResponse(CategoryBase):
    """Schema for category response"""
    id: int
    user_id: int

    class Config:
        from_attributes = True
