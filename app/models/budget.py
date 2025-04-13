from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    DECIMAL,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    month = Column(
        Integer, nullable=False
    )  # Assuming you'll handle the CHECK constraint in the database
    year = Column(Integer, nullable=False)

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")

    #  You might need to add a UniqueConstraint here, but it's often handled at the database level
    #  __table_args__ = (
    #      UniqueConstraint('user_id', 'category_id', 'month', 'year', name='unique_budget'),
    #  )
