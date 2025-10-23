import os
from app import create_app
from app.services.auth_service import AuthService
from app.database.db import Base, engine, SessionLocal
from app.models.user import User
from app.models.task import Task
from app.models.task_log import TaskLog

env = os.getenv('FLASK_ENV', 'production')
app = create_app(env)

if __name__ == '__main__':
    import sys
    if not hasattr(sys, '_called_from_reload'):
        try:
            AuthService.create_default_user()
        except Exception as e:
            print(f"User creation: {e}")

    print("Starting Flask...")
    print(f"Environment: {env}")
    print(f"Server: http://localhost:5000")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )

