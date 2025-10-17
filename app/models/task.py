from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base 

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    assigned_to = Column(String(100), nullable=False)
    status = Column(String(20), default="Not_Started")
    priority = Column(String(20), default="Medium")
    start_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, default=datetime.utcnow)
    completed_date = Column(DateTime, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = relationship("User", back_populates="tasks_created")
    logs = relationship("TaskLog", back_populates="task", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "priority": self.priority,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_date": self.completed_date.isoformat() if self.completed_date else None,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
