import datetime
from uuid import UUID
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from core.database.postgres import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="todo")  # e.g., "todo", "in_progress", "done"
    board_id = Column(UUID, ForeignKey("boards.id"), nullable=False)
    assignee_id = Column(UUID, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)

    board = relationship("Board", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")