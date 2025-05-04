from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID  # Import PostgreSQL-specific UUID
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean
from core.database.postgres import Base
from sqlalchemy.orm import relationship

class Board(Base):
    __tablename__ = "boards"

    id= Column(UUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="boards")
    tasks = relationship("Task", back_populates="board")

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

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    boards = relationship("Board", back_populates="owner")
    tasks = relationship("Task", back_populates="assignee")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True),primary_key=True, index=True)
    project_name = Column(String(50), unique=True, index= True, nullable=False)
    description = Column(String(250), nullable=True, index=True)
    created_at = Column(DateTime,nullable=False, index=True, default=datetime.utcnow)
    