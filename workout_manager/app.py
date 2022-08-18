from flask import Flask, request, jsonify
from service import (exerciseService, userService)
from models import Schema

from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import json

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


@app.route("/exercise/<item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id):
    return jsonify(exerciseService().update(item_id, request.get_json()))

@app.route("/exercise/<item_id>", methods=["GET"])
@jwt_required()
def get_item(item_id):
    return jsonify(exerciseService().get_by_id(item_id))

@app.route("/exercise/<item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(item_id):
    return jsonify(exerciseService().delete(item_id))

if __name__ == "__main__":
    Schema()
    app.run(debug=True, host='0.0.0.0', port=8888)