import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from app.config import Config

config = Config()

def generate_token(user_id: int, username: str) -> str:
    """Generate JWT token for authenticated user"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + config.JWT_ACCESS_TOKEN_EXPIRES,
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, config.JWT_SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token: str) -> dict:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')

def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Token format invalid. Use: Bearer <token>'
                }), 401
        if not token:
            return jsonify({
                'success': False,
                'message': 'Authentication token is missing'
            }), 401
        try:
            payload = decode_token(token)
            request.current_user = payload
        except Exception as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated