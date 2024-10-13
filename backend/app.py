from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from serverless_wsgi import handle_request

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://task-list-fs.netlify.com"}})

# Use SQLite for Netlify deployment
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models after db initialization
from models import Task

# Import routes after initializing app and db
from routes import *

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

def handler(event, context):
    return handle_request(app, event, context)

@app.cli.command("init-db")
def init_db():
    create_tables()
    print("Database initialized.")

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
