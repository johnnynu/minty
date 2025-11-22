"""Transaction model"""

from datetime import date as date_type
from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.database import Base


class Transaction(Base):
    """Financial transaction"""

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    date = Column(Date, nullable=False, index=True)
    payee = Column(String, nullable=False)
    amount = Column(Numeric(precision=15, scale=2), nullable=False)
    memo = Column(String, nullable=True)
    cleared = Column(Boolean, default=False, nullable=False)

    # Relationships
    user = relationship("User", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

    __table_args__ = (
        Index("idx_transactions_user_id", "user_id"),
        Index("idx_transactions_date", "date"),
    )
