"""Budget allocation model"""

from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.database import Base


class BudgetAllocation(Base):
    """Monthly budget allocation for a category"""

    __tablename__ = "budget_allocations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    month = Column(String, nullable=False)  # Format: YYYY-MM
    amount = Column(Numeric(precision=15, scale=2), nullable=False)

    # Relationships
    user = relationship("User", back_populates="budget_allocations")
    category = relationship("Category", back_populates="budget_allocations")

    __table_args__ = (
        Index("idx_budget_allocations_user_category", "user_id", "category_id", "month"),
    )
