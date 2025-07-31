from flask import Flask
sapp = Flask(__name__)

@sapp.route("/")
def hello():
    return "HELLO"