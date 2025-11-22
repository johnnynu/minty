"""Budget allocation CRUD endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware import get_current_user
from app.models import User, BudgetAllocation, Category
from app.schemas import (
    BudgetAllocationCreate,
    BudgetAllocationUpdate,
    BudgetAllocationResponse,
)

router = APIRouter(prefix="/budget", tags=["budget"])


@router.get("/", response_model=list[BudgetAllocationResponse])
async def list_budget_allocations(
    month: str | None = Query(None, pattern=r"^\d{4}-\d{2}$"),
    category_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List budget allocations for the current user with optional filters"""
    query = db.query(BudgetAllocation).filter(
        BudgetAllocation.user_id == current_user.id
    )

    if month:
        query = query.filter(BudgetAllocation.month == month)
    if category_id:
        query = query.filter(BudgetAllocation.category_id == category_id)

    allocations = query.all()
    return allocations


@router.get("/{allocation_id}", response_model=BudgetAllocationResponse)
async def get_budget_allocation(
    allocation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific budget allocation by ID"""
    allocation = db.query(BudgetAllocation).filter(
        BudgetAllocation.id == allocation_id,
        BudgetAllocation.user_id == current_user.id
    ).first()

    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget allocation not found"
        )

    return allocation


@router.post("/", response_model=BudgetAllocationResponse, status_code=status.HTTP_201_CREATED)
async def create_budget_allocation(
    allocation_data: BudgetAllocationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new budget allocation"""
    # Verify category belongs to user
    category = db.query(Category).filter(
        Category.id == allocation_data.category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Check if allocation already exists for this category/month
    existing = db.query(BudgetAllocation).filter(
        BudgetAllocation.user_id == current_user.id,
        BudgetAllocation.category_id == allocation_data.category_id,
        BudgetAllocation.month == allocation_data.month
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Budget allocation already exists for this category and month"
        )

    allocation = BudgetAllocation(
        **allocation_data.model_dump(),
        user_id=current_user.id
    )
    db.add(allocation)
    db.commit()
    db.refresh(allocation)
    return allocation


@router.put("/{allocation_id}", response_model=BudgetAllocationResponse)
async def update_budget_allocation(
    allocation_id: int,
    allocation_data: BudgetAllocationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing budget allocation"""
    allocation = db.query(BudgetAllocation).filter(
        BudgetAllocation.id == allocation_id,
        BudgetAllocation.user_id == current_user.id
    ).first()

    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget allocation not found"
        )

    update_data = allocation_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(allocation, field, value)

    db.commit()
    db.refresh(allocation)
    return allocation


@router.delete("/{allocation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget_allocation(
    allocation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a budget allocation"""
    allocation = db.query(BudgetAllocation).filter(
        BudgetAllocation.id == allocation_id,
        BudgetAllocation.user_id == current_user.id
    ).first()

    if not allocation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget allocation not found"
        )

    db.delete(allocation)
    db.commit()
    return None
