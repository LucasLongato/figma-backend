from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from models import db
from models.task import Task
from models.user import User
from flask_login import login_required, current_user

task_bp = Blueprint('task_bp', __name__)

@task_bp.route("/dashboard")
@login_required
def dashboard():
    # Fetch tasks assigned to the current user
    tasks = current_user.tasks
    return render_template('dashboard.html', tasks=tasks)

@task_bp.route("/tasks/new", methods=['POST'])
@login_required
def new_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    # Validate the input
    if not title or not description:
        return jsonify({'error': 'Title and description are required!'}), 400

    # Create new task, passing current_user.id as the owner
    task = Task(title=title, description=description, owner_id=current_user.id)
    db.session.add(task)
    db.session.commit()

    # Return the created task as JSON
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'owner_id': task.owner_id  # Return the owner's ID
    }), 201

@task_bp.route("/tasks/<int:task_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Ensure the current user is assigned to the task or is authorized to edit it
    if current_user not in task.users:
        flash('You are not authorized to edit this task', 'danger')
        return redirect(url_for('task_bp.dashboard'))
    
    if request.method == 'POST':
        task.title = request.form.get('title')
        task.description = request.form.get('description')
        task.status = request.form.get('status')
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('task_bp.dashboard'))
    
    return render_template('edit_task.html', task=task)

@task_bp.route("/tasks/<int:task_id>/delete", methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    # Ensure the current user is assigned to the task or is authorized to delete it
    if current_user not in task.users:
        flash('You are not authorized to delete this task', 'danger')
        return redirect(url_for('task_bp.dashboard'))
    
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('task_bp.dashboard'))

@task_bp.route("/tasks/<int:task_id>/assign", methods=['POST'])
@login_required
def assign_task(task_id):
    task = Task.query.get_or_404(task_id)
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)

    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('task_bp.dashboard'))
    
    if task not in user.tasks:
        user.tasks.append(task)
        db.session.commit()
        flash('Task assigned to user successfully!', 'success')
    else:
        flash('Task is already assigned to this user', 'warning')

    return redirect(url_for('task_bp.dashboard'))

@task_bp.route("/tasks/<int:task_id>/deassign", methods=['POST'])
@login_required
def deassign_task(task_id):
    task = Task.query.get_or_404(task_id)
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)

    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('task_bp.dashboard'))

    if task in user.tasks:
        user.tasks.remove(task)
        db.session.commit()
        flash('Task deassigned from user successfully!', 'success')
    else:
        flash('Task is not assigned to this user', 'warning')

    return redirect(url_for('task_bp.dashboard'))

@task_bp.route("/tasks", methods=['GET'])
def get_all_tasks():
    # Fetch all tasks from the database
    tasks = Task.query.all()

    # Return tasks data
    task_list = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "owner_id": task.owner_id
        }
        for task in tasks
    ]
    
    return jsonify(task_list), 200