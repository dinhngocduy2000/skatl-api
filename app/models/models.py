from datetime import datetime
from typing import List, Optional
from sqlalchemy.dialects.postgresql import UUID  # Import PostgreSQL-specific UUID
from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, Boolean
from schemas.domain.user import IUser
from core.database.postgres import Base
from sqlalchemy.orm import relationship


# class Board(Base):
#     __tablename__ = "boards"

#     id = Column(UUID(as_uuid=True), primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     description = Column(String)
#     owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     owner = relationship("User", back_populates="boards")
#     tasks = relationship("Task", back_populates="board")


# class Task(Base):
#     __tablename__ = "tasks"

#     id = Column(UUID, primary_key=True, index=True)
#     title = Column(String, nullable=False)
#     description = Column(String)
#     # e.g., "todo", "in_progress", "done"
#     status = Column(String, default="todo")
#     board_id = Column(UUID, ForeignKey("boards.id"), nullable=False)
#     assignee_id = Column(UUID, ForeignKey("users.id"), nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     due_date = Column(DateTime, nullable=True)

#     board = relationship("Board", back_populates="tasks")
#     assignee = relationship("User", back_populates="tasks")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    # Other user fields...

    # Optional: Define the inverse relationship
    project = relationship("Project", back_populates="members")
    # boards = relationship("Board", back_populates="owner")
    # tasks = relationship("Task", back_populates="assignee")
    project_users = relationship("ProjectUsers", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    project_name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(250), nullable=True, index=True)
    created_at = Column(DateTime, nullable=True, index=True, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=True,
        index=True,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    members = relationship("User", back_populates="project")
    project_users = relationship("ProjectUsers", back_populates="project")


class ProjectUsers(Base):
    __tablename__ = "project_users"

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    project = relationship("Project", back_populates="project_users")
    user = relationship("User", back_populates="project_users")
