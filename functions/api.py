from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from serverless_wsgi import handle_request

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Use SQLite for Netlify deployment
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    entityName = db.Column(db.String(100))
    taskType = db.Column(db.String(100))
    date = db.Column(db.String(10))
    time = db.Column(db.String(5))
    contactPerson = db.Column(db.String(100))
    status = db.Column(db.String(20))
    note = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'entityName': self.entityName,
            'taskType': self.taskType,
            'date': self.date,
            'time': self.time,
            'contactPerson': self.contactPerson,
            'status': self.status,
            'note': self.note,
            'done': self.done
        }

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
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

def handler(event, context):
    return handle_request(app, event, context)

if __name__ == '__main__':
    app.run(debug=True)
