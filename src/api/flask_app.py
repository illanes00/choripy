from flask import Flask, jsonify
flask_app = Flask(__name__)

@flask_app.route("/")
def hello():
    return jsonify(msg="Hola Flask 🌮")
