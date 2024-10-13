from flask import Flask
import serverless_http

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Flask!'

handler = serverless_http.get_handler(app)
