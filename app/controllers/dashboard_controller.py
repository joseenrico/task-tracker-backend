from flask import Blueprint, jsonify
from app.services.dashboard_service import DashboardService
from app.utils.jwt_utils import token_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/statistics', methods=['GET'])
@token_required
def get_statistics():
    """Get dashboard statistics"""
    try:
        stats = DashboardService.get_statistics()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500
