from flask import Flask, jsonify
from flask_cors import CORS
from app.config import config  
from app.database.db import engine, Base, SessionLocal
from app.controllers.auth_controller import auth_bp
from app.controllers.task_controller import task_bp
from app.controllers.dashboard_controller import dashboard_bp

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)

    # --- Load configuration ---
    conf = config.get(config_name, config['default'])
    app.config.from_object(conf)

    # --- Initialize database (create tables) ---
    Base.metadata.create_all(bind=engine)

    # --- Setup CORS ---
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', ['http://localhost:5173']),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # --- Register blueprints ---
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(task_bp, url_prefix='/api/tasks')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    # --- Health check ---
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'success': True, 'message': 'Server is running', 'status': 'healthy'}), 200

    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'success': True,
            'message': 'Team Task Tracker API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth',
                'tasks': '/api/tasks',
                'dashboard': '/api/dashboard'
            }
        }), 200

    # --- Error handlers ---
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'message': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

    return app
