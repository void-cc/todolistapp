from flask import Blueprint, request, jsonify, session
from database_interactions import todo_interacts as ti
from functools import wraps

api = Blueprint('api', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@api.route('/todos', methods=['GET'])
@login_required
def get_todos():
    user_id = session['user_id']
    todos = ti.get_todo_function(user_id)
    return jsonify(todos)

@api.route('/todos', methods=['POST'])
@login_required
def add_todo():
    user_id = session['user_id']
    data = request.get_json()
    ti.add_to_todo(
        todo_text=data['todo_text'],
        user_id=user_id,
        todo_date=data.get('todo_date'),
        tags=data.get('tags')
    )
    return jsonify({'message': 'Todo added successfully'}), 201

@api.route('/todos/<int:todo_id>', methods=['PUT'])
@login_required
def update_todo(todo_id):
    todo = ti.get_todo_by_id(todo_id)
    if not todo or todo.user_id != session['user_id']:
        return jsonify({'message': 'Todo not found or unauthorized'}), 404

    data = request.get_json()
    if 'todo_done' in data:
        ti.change_todo_done(todo_id, data['todo_done'])
    if 'todo_text' in data:
        ti.change_todo_text(todo_id, data['todo_text'])
    if 'todo_date' in data:
        ti.change_todo_date(todo_id, data['todo_date'])
    if 'tags' in data:
        ti.change_todo_tags(todo_id, data['tags'])
    return jsonify({'message': 'Todo updated successfully'})

@api.route('/todos/<int:todo_id>', methods=['DELETE'])
@login_required
def delete_todo(todo_id):
    todo = ti.get_todo_by_id(todo_id)
    if not todo or todo.user_id != session['user_id']:
        return jsonify({'message': 'Todo not found or unauthorized'}), 404

    ti.delete_todo(todo_id)
    return jsonify({'message': 'Todo deleted successfully'})
