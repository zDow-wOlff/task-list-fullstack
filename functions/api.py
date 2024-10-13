from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from serverless_wsgi import handle_request

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Use SQLite for Netlify deployment
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/tasks.db' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models and routes
from models import Task
from routes import *

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
    print(f"Received task data: {data}")
    print(f"New task created: {new_task.to_dict()}")
    return jsonify(new_task.to_dict()), 201

def create_tables():
    with app.app_context():
        db.create_all()

def handler(event, context):
    create_tables()
    return handle_request(app, event, context)

if __name__ == '__main__':
    app.run(debug=True)
