from flask import Flask

app = Flask(__name__)
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/")
def home():
    print("Server received a request")
    return "Hello from the web application"

@app.route("/welcome")
def hello():
    return "You reached the hello route"