from sqlalchemy.orm import Session
from sqlalchemy import func, case, cast, Float
from app.database.db import SessionLocal
from app.models.task import Task
from app.models.task_log import TaskLog
from app.models.user import User

class DashboardService:
    @staticmethod
    def get_statistics():
        """Get dashboard statistics for overview"""
        db: Session = SessionLocal()
        try:
            stats_query = db.query(
                func.count(Task.id),
                func.count(case((Task.status == 'Not_Started', 1))),
                func.count(case((Task.status == 'In_Progress', 1))),
                func.count(case((Task.status == 'Completed', 1))),
                func.count(case((Task.due_date < func.current_date(), Task.status != 'Completed')))
            ).one()

            stats = {
                'total_tasks': stats_query[0],
                'not_started': stats_query[1],
                'in_progress': stats_query[2],
                'completed': stats_query[3],
                'overdue': stats_query[4]
            }

            team_activity_query = db.query(
                Task.assigned_to,
                func.count(Task.id),
                func.count(case((Task.status == 'Completed', 1))),
                func.count(case((Task.status == 'In_Progress', 1))),
                (cast(func.count(case((Task.status == 'Completed', 1))), Float) /
                 func.nullif(func.count(Task.id), 0) * 100)
            ).group_by(Task.assigned_to).order_by(func.count(case((Task.status == 'Completed', 1))).desc()).all()

            team_activity = [
                {
                    'assigned_to': row[0],
                    'total_tasks': row[1],
                    'completed_tasks': row[2],
                    'ongoing_tasks': row[3],
                    'completion_rate': float(row[4]) if row[4] else 0
                } for row in team_activity_query
            ]

            recent_activities_query = (
                db.query(
                    TaskLog.id,
                    Task.title,
                    TaskLog.old_status,
                    TaskLog.new_status,
                    User.full_name,
                    TaskLog.changed_at
                )
                .join(Task, Task.id == TaskLog.task_id)
                .outerjoin(User, User.id == TaskLog.changed_by)
                .order_by(TaskLog.changed_at.desc())
                .limit(10)
                .all()
            )

            recent_activities = [
                {
                    'id': row[0],
                    'task_title': row[1],
                    'old_status': row[2],
                    'new_status': row[3],
                    'changed_by': row[4],
                    'changed_at': row[5].isoformat() if row[5] else None
                } for row in recent_activities_query
            ]

            return {
                'statistics': stats,
                'team_activity': team_activity,
                'recent_activities': recent_activities
            }

        finally:
            db.close()
