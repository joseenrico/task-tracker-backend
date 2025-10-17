from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login endpoint"""
    data = request.get_json() or {}

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'success': False,
            'message': 'Username and password are required'
        }), 400

    try:
        result, error = AuthService.login(username, password)
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 401

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': result
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500
