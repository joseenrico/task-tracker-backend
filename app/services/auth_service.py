from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.jwt_utils import generate_token
from app.database.db import SessionLocal

class AuthService:
    @staticmethod
    def login(username: str, password: str):
        """Authenticate user and generate token"""
        db: Session = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if not user or not check_password_hash(user.password_hash, password):
                return None, "Invalid username or password"
            
            token = generate_token(user.id, user.username)
            return {'access_token': token, 'user': user.to_dict()}, None
        finally:
            db.close()
    
    @staticmethod
    def create_default_user():
        """Create default admin user (for initial setup)"""
        db: Session = SessionLocal()
        try:
            existing_user = db.query(User).filter(User.username == "admin").first()
            if not existing_user:
                password_hash = generate_password_hash('admin123')
                user = User(
                    username="admin",
                    email="admin@herobusana.com",
                    password_hash=password_hash,
                    full_name="Project Manager",
                    role="project_manager"
                )
                db.add(user)
                db.commit()
        finally:
            db.close()
