import datetime
from uuid import UUID
from sqlalchemy import Column, DateTime, ForeignKey, String
from core.database.postgres import Base
from sqlalchemy.orm import relationship

class Board(Base):
    __tablename__ = "boards"

    id :UUID= Column(UUID, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    owner_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="boards")
    tasks = relationship("Task", back_populates="board")