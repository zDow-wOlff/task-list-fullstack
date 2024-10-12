from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample data (replace this with your database later)
task = [
    {"id": 1, "title": "Python Basics", "description": "Test your knowledge of Python fundamentals"},
    {"id": 2, "title": "Angular Fundamentals", "description": "Assess your understanding of Angular core concepts"}
]

@app.route('/api/task', methods=['GET'])
def get_task():
    return jsonify(task)

@app.route('/api/task', methods=['POST'])
def add_task():
    new_task = request.json
    new_task['id'] = len(task) + 1
    task.append(new_task)
    return jsonify(new_task), 201

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(description=data['description'], done=data['done'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Task List API'})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Retrieve all tasks
    ...
    return response

@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Retrieve a specific task by ID
    ...
    return response

if __name__ == '__main__':
    app.run(debug=True)