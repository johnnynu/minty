"""Category models"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class CategoryGroup(Base):
    """Category group for organizing spending categories"""

    __tablename__ = "category_groups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    # Relationships
    user = relationship("User", back_populates="category_groups")
    categories = relationship("Category", back_populates="category_group", cascade="all, delete-orphan")


class Category(Base):
    """Spending/income category"""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_group_id = Column(Integer, ForeignKey("category_groups.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    # Relationships
    user = relationship("User", back_populates="categories")
    category_group = relationship("CategoryGroup", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")
    budget_allocations = relationship("BudgetAllocation", back_populates="category", cascade="all, delete-orphan")
