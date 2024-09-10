# routes/user_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from models import db
from models.task import Task
from models.user import User
from flask_login import login_user, current_user, logout_user

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    # Check if the user already exists
    user_exists = User.query.filter_by(login=login).first()
    if user_exists:
        return jsonify({"error": "User already exists"}), 400

    # Create a new user
    new_user = User(login=login, password=password)
    
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    # Find the user by login
    user = User.query.filter_by(login=login).first()
    
    if user and user.check_password(password):
        # Log the user in
        login_user(user)
        return jsonify({"message": f"Logged in as {login}"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@user_bp.route('/all', methods=['GET'])
def get_all_users():
    # Fetch all users from the database
    users = User.query.all()

    # Return user data with login and hashed password
    user_list = [
        {
            "login": user.login,
            "password": user.password  # This will return the hashed password
        }
        for user in users
    ]
    
    return jsonify(user_list), 200

# @user_bp.route('/assign_task', methods=['POST'])
# def assign_task():
#     data = request.get_json()
#     user_id = data.get('user_id')
#     task_id = data.get('task_id')

#     # Fetch user and task
#     user = User.query.get(user_id)
#     task = Task.query.get(task_id)

#     if not user or not task:
#         return jsonify({"error": "User or task not found"}), 404

#     # Assign task to user
#     if task not in user.tasks:
#         user.tasks.append(task)
#         db.session.commit()
#         return jsonify({"message": "Task assigned successfully"}), 200
#     else:
#         return jsonify({"error": "Task already assigned to user"}), 400

# @user_bp.route('/deassign_task', methods=['POST'])
# def deassign_task():
#     data = request.get_json()
#     user_id = data.get('user_id')
#     task_id = data.get('task_id')

#     # Fetch user and task
#     user = User.query.get(user_id)
#     task = Task.query.get(task_id)

#     if not user or not task:
#         return jsonify({"error": "User or task not found"}), 404

#     # Deassign task from user
#     if task in user.tasks:
#         user.tasks.remove(task)
#         db.session.commit()
#         return jsonify({"message": "Task deassigned successfully"}), 200
#     else:
#         return jsonify({"error": "Task not assigned to user"}), 400