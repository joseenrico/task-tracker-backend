from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.task_log import TaskLog
from app.models.task import Task
from app.models.user import User
from app.database.db import SessionLocal

class TaskLogService:
    @staticmethod
    def create_log(
        task_id: int,
        old_status: Optional[str],
        new_status: str,
        user_id: int,
        reason: Optional[str] = None,
    ) -> TaskLog:
        """Create a task log entry"""
        db: Session = SessionLocal()
        try:
            log = TaskLog(
                task_id=task_id,
                old_status=old_status,
                new_status=new_status,
                changed_by=user_id,
                change_reason=reason
            )
            db.add(log)
            db.commit()
            db.refresh(log)
            return log
        finally:
            db.close()

    @staticmethod
    def get_logs_by_task(task_id: int) -> List[TaskLog]:
        """Get all logs for a specific task"""
        db: Session = SessionLocal()
        try:
            logs = (
                db.query(TaskLog)
                .filter(TaskLog.task_id == task_id)
                .order_by(TaskLog.changed_at.desc())
                .all()
            )
            return logs
        finally:
            db.close()

    @staticmethod
    def get_all_logs(limit: int = 50) -> List[dict]:
        """Get all logs with task and user details"""
        db: Session = SessionLocal()
        try:
            logs = (
                db.query(TaskLog)
                .join(Task, TaskLog.task_id == Task.id)
                .outerjoin(User, TaskLog.changed_by == User.id)
                .order_by(TaskLog.changed_at.desc())
                .limit(limit)
                .all()
            )

            return [
                {
                    "id": log.id,
                    "task_id": log.task_id,
                    "task_title": log.task.title if log.task else None,
                    "old_status": log.old_status,
                    "new_status": log.new_status,
                    "changed_by": log.changer.full_name if log.changer else None,
                    "change_reason": log.change_reason,
                    "changed_at": log.changed_at.isoformat() if log.changed_at else None
                }
                for log in logs
            ]
        finally:
            db.close()
