from flask import jsonify, request
from app import app, db
from models import Task

@app.route('/tasks', methods=['GET'])
def get_tasks():
    query = Task.query

    # Filtering
    status = request.args.get('status')
    team_member = request.args.get('teamMember')
    task_type = request.args.get('taskType')
    entity_name = request.args.get('entityName')
    date = request.args.get('date')

    if status:
        query = query.filter(Task.status == status)
    if team_member:
        query = query.filter(Task.contactPerson.ilike(f'%{team_member}%'))
    if task_type:
        query = query.filter(Task.taskType.ilike(f'%{task_type}%'))
    if entity_name:
        query = query.filter(Task.entityName.ilike(f'%{entity_name}%'))
    if date:
        query = query.filter(Task.date == date)

    # Sorting
    sort_by = request.args.get('sortBy', 'id')
    sort_order = request.args.get('sortOrder', 'asc')

    if sort_order == 'desc':
        query = query.order_by(getattr(Task, sort_by).desc())
    else:
        query = query.order_by(getattr(Task, sort_by))

    tasks = query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(
        description=data['description'],
        entityName=data.get('entityName'),
        taskType=data.get('taskType'),
        date=data.get('date'),
        time=data.get('time'),
        contactPerson=data.get('contactPerson'),
        status=data.get('status'),
        note=data.get('note'),
        done=data.get('done', False)
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    for field in ['description', 'entityName', 'taskType', 'date', 'time', 'contactPerson', 'status', 'note', 'done']:
        if field in data:
            setattr(task, field, data[field])
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Task List API'})
