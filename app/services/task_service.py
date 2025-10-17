from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.task import Task
from app.models.task_log import TaskLog
from app.models.user import User
from app.database.db import SessionLocal

class TaskService:

    @staticmethod
    def get_all_tasks(status: Optional[str] = None, assigned_to: Optional[str] = None) -> List[Task]:
        """Get all tasks with optional filters"""
        with SessionLocal() as session:
            query = session.query(Task)
            if status:
                query = query.filter(Task.status == status)
            if assigned_to:
                query = query.filter(Task.assigned_to == assigned_to)
            return query.order_by(Task.created_at.desc()).all()

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        with SessionLocal() as session:
            return session.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def create_task(task_data: dict, user_id: int) -> Optional[Task]:
        with SessionLocal() as session:
            task = Task(
                title=task_data.get("title"),
                description=task_data.get("description"),
                assigned_to=task_data.get("assigned_to"),
                status=task_data.get("status", "Not_Started"),
                priority=task_data.get("priority", "Medium"),
                start_date=datetime.fromisoformat(task_data.get("start_date")) if task_data.get("start_date") else None,
                due_date=datetime.fromisoformat(task_data.get("due_date")) if task_data.get("due_date") else None,
                created_by=user_id
            )
            session.add(task)
            session.flush()
            log = TaskLog(
                task_id=task.id,
                old_status=None,
                new_status=task.status,
                changed_by=user_id
            )
            session.add(log)
            session.commit()
            return task

    @staticmethod
    def update_task(task_id: int, task_data: dict, user_id: int) -> Optional[Task]:
        with SessionLocal() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return None
        old_status = task.status
        task.title = task_data.get("title", task.title)
        task.description = task_data.get("description", task.description)
        task.assigned_to = task_data.get("assigned_to", task.assigned_to)
        task.status = task_data.get("status", task.status)
        task.priority = task_data.get("priority", task.priority)
        start_date = task_data.get("start_date")
        if start_date and isinstance(start_date, str):
            task.start_date = datetime.fromisoformat(start_date)
        due_date = task_data.get("due_date")
        if due_date and isinstance(due_date, str):
            task.due_date = datetime.fromisoformat(due_date)
        if task.status == "Completed" and not task.completed_date:
            task.completed_date = datetime.utcnow()
        if old_status != task.status:
            log = TaskLog(
                task=task, 
                old_status=old_status,
                new_status=task.status,
                changed_by=user_id,
                change_reason=task_data.get("change_reason", f"Status changed from {old_status} to {task.status}")
            )
            session.add(log)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task(task_id: int) -> bool:
        with SessionLocal() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            if not task:
                return False
            session.delete(task)
            session.commit()
            return True
