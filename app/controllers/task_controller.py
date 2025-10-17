from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService
from app.services.task_log_service import TaskLogService
from app.utils.jwt_utils import token_required

task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')


@task_bp.route('', methods=['GET'])
@token_required
def get_tasks():
    """Get all tasks with optional filters"""
    try:
        status = request.args.get('status')
        assigned_to = request.args.get('assigned_to')
        tasks = TaskService.get_all_tasks(status=status, assigned_to=assigned_to)
        return jsonify({
            "success": True,
            "data": [task.to_dict() for task in tasks]
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@task_bp.route('/<int:task_id>', methods=['GET'])
@token_required
def get_task(task_id):
    try:
        task = TaskService.get_task_by_id(task_id)
        if not task:
            return jsonify({"success": False, "message": "Task not found"}), 404
        return jsonify({"success": True, "data": task.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@task_bp.route('', methods=['POST'])
@token_required
def create_task():
    try:
        data = request.get_json()
        user_id = request.current_user['user_id']
        if not data.get('title') or not data.get('assigned_to'):
            return jsonify({"success": False, "message": "Title and assigned_to are required"}), 400
        task = TaskService.create_task(data, user_id)
        return jsonify({"success": True, "message": "Task created successfully", "data": task.to_dict()}), 201
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@task_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    try:
        data = request.get_json()
        user_id = request.current_user['user_id']
        task = TaskService.update_task(task_id, data, user_id)
        if not task:
            return jsonify({"success": False, "message": "Task not found"}), 404
        return jsonify({"success": True, "message": "Task updated successfully", "data": task.to_dict()}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@task_bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):
    try:
        success = TaskService.delete_task(task_id)
        if not success:
            return jsonify({"success": False, "message": "Task not found"}), 404
        return jsonify({"success": True, "message": "Task deleted successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@task_bp.route('/<int:task_id>/logs', methods=['GET'])
@token_required
def get_task_logs(task_id):
    try:
        logs = TaskLogService.get_logs_by_task(task_id)
        return jsonify({"success": True, "data": [log.to_dict() for log in logs]}), 200
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500
