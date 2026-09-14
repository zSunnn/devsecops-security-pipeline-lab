from flask import Flask

app = Flask(__name__)

# Deliberate dummy value for testing the CI security gate.
password = "lab-demo-not-a-real-password"

@app.route("/")
def home():
    print("Server received a request")
    return "Hello from the web application"

@app.route("/welcome")
def hello():
    return "You reached the hello route"