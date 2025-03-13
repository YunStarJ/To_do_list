# To-do 관련 API

from flask import Blueprint, request, jsonify
from models import db
from models.todo import Todo
from flask_jwt_extended import jwt_required, get_jwt_identity

todo_bp = Blueprint("todo", __name__)

# 할 일 추가 (Create)
@todo_bp.route("/todos", methods=["POST"])
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()  # JWT에서 현재 사용자 ID 가져오기
    data = request.get_json()
    
    new_todo = Todo(
        title=data["title"],
        description=data.get("description", ""),
        completed=False,
        user_id=user_id
    )
    
    db.session.add(new_todo)
    db.session.commit()
    
    return jsonify({"message": "To-Do created successfully", "todo": new_todo.to_dict()}), 201


# 할 일 목록 조회 (Read)
@todo_bp.route("/todos", methods=["GET"])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id).all()
    return jsonify([todo.to_dict() for todo in todos]), 200


# 할 일 수정 (Update)
@todo_bp.route("/todos/<int:todo_id>", methods=["PUT"])
@jwt_required()
def update_todo(todo_id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    if not todo:
        return jsonify({"message": "To-Do not found"}), 404

    data = request.get_json()
    todo.title = data.get("title", todo.title)
    todo.description = data.get("description", todo.description)
    todo.completed = data.get("completed", todo.completed)

    db.session.commit()
    return jsonify({"message": "To-Do updated successfully", "todo": todo.to_dict()}), 200


# 할 일 삭제 (Delete)
@todo_bp.route("/todos/<int:todo_id>", methods=["DELETE"])
@jwt_required()
def delete_todo(todo_id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    if not todo:
        return jsonify({"message": "To-Do not found"}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "To-Do deleted successfully"}), 200
