from flask import Flask, jsonify
from flask_cors import CORS
from serverless_wsgi import handle_request

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Task List API'})

def handler(event, context):
    return handle_request(app, event, context)
