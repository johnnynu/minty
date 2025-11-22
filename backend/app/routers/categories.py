"""Category and Category Group CRUD endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware import get_current_user
from app.models import User, Category, CategoryGroup
from app.schemas import (
    CategoryGroupCreate,
    CategoryGroupUpdate,
    CategoryGroupResponse,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)

router = APIRouter(prefix="/categories", tags=["categories"])


# Category Group endpoints
@router.get("/groups", response_model=list[CategoryGroupResponse])
async def list_category_groups(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all category groups for the current user"""
    groups = db.query(CategoryGroup).filter(
        CategoryGroup.user_id == current_user.id
    ).order_by(CategoryGroup.sort_order).all()
    return groups


@router.get("/groups/{group_id}", response_model=CategoryGroupResponse)
async def get_category_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific category group by ID"""
    group = db.query(CategoryGroup).filter(
        CategoryGroup.id == group_id,
        CategoryGroup.user_id == current_user.id
    ).first()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category group not found"
        )

    return group


@router.post("/groups", response_model=CategoryGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_category_group(
    group_data: CategoryGroupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new category group"""
    group = CategoryGroup(
        **group_data.model_dump(),
        user_id=current_user.id
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


@router.put("/groups/{group_id}", response_model=CategoryGroupResponse)
async def update_category_group(
    group_id: int,
    group_data: CategoryGroupUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing category group"""
    group = db.query(CategoryGroup).filter(
        CategoryGroup.id == group_id,
        CategoryGroup.user_id == current_user.id
    ).first()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category group not found"
        )

    update_data = group_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(group, field, value)

    db.commit()
    db.refresh(group)
    return group


@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a category group"""
    group = db.query(CategoryGroup).filter(
        CategoryGroup.id == group_id,
        CategoryGroup.user_id == current_user.id
    ).first()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category group not found"
        )

    db.delete(group)
    db.commit()
    return None


# Category endpoints
@router.get("/", response_model=list[CategoryResponse])
async def list_categories(
    group_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all categories for the current user, optionally filtered by group"""
    query = db.query(Category).filter(Category.user_id == current_user.id)

    if group_id:
        query = query.filter(Category.category_group_id == group_id)

    categories = query.order_by(Category.sort_order).all()
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific category by ID"""
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new category"""
    # Verify category group belongs to user
    group = db.query(CategoryGroup).filter(
        CategoryGroup.id == category_data.category_group_id,
        CategoryGroup.user_id == current_user.id
    ).first()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category group not found"
        )

    category = Category(
        **category_data.model_dump(),
        user_id=current_user.id
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing category"""
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a category"""
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()
    return None
