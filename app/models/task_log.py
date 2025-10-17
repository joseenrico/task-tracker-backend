from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db import Base 

class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    old_status = Column(String(20))
    new_status = Column(String(20), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    change_reason = Column(Text)
    changed_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="logs")
    user = relationship("User", back_populates="task_logs")

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "old_status": self.old_status,
            "new_status": self.new_status,
            "changed_by": self.changed_by,
            "change_reason": self.change_reason,
            "changed_at": self.changed_at.isoformat() if self.changed_at else None
        }
