from flask import Flask, request, jsonify
from service import (exerciseService, userService)
from models import Schema

from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import json
import time

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

@app.route('/register', methods=('POST',))
def register():
    return userService().register(request.get_json())

@app.route('/login', methods=('POST',))
def login():
    return userService().login(request.get_json())

@app.route("/exercise", methods=["GET"])
@jwt_required()
def list_exercises():
    return jsonify(exerciseService().list())


@app.route("/exercise", methods=["POST"])
@jwt_required()
def create_exercise():
    return jsonify(exerciseService().create(request.get_json()))


@app.route("/exercise/<exercise_id>", methods=["PUT"])
@jwt_required()
def update_item(exercise_id):
    return jsonify(exerciseService().update(exercise_id, request.get_json()))

@app.route("/exercise/<exercise_id>", methods=["GET"])
@jwt_required()
def get_item(exercise_id):
    return jsonify(exerciseService().get_by_id(exercise_id))

@app.route("/exercise/<exercise_id>", methods=["DELETE"])
@jwt_required()
def delete_item(exercise_id):
    return jsonify(exerciseService().delete_by_id(exercise_id))

@app.route("/exercise/name/<exercise_name>", methods=["GET"])
@jwt_required()
def get_item_by_name(exercise_name):
    return jsonify(exerciseService().get_by_name(exercise_name))


if __name__ == "__main__":
    time.sleep(5)
    Schema()
    app.run(debug=True, host='0.0.0.0', port=8888)