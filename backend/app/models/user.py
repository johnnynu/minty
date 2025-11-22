"""User model"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """User account linked to Clerk authentication"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    clerk_user_id = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    category_groups = relationship("CategoryGroup", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
    budget_allocations = relationship("BudgetAllocation", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_users_clerk_id", "clerk_user_id"),
    )
