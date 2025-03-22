from uuid import UUID
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from core.database.postgres import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    boards = relationship("Board", back_populates="owner")
    tasks = relationship("Task", back_populates="assignee")