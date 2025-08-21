from flask import Blueprint, request, jsonify
from services.userService import create_user, verify_user
from models.userModel import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.json
    name, email, password = data["name"], data["email"], data["password"]
    user = User(name=name, email=email, password=password, assets=[], virtualBalance=10000)
    response = create_user(user)
    if response["success"]:
        return jsonify({"message": response["message"]}), 201
    return jsonify({"error": response["message"]}), 400

@auth_bp.post("/login")
def login():
    data = request.json
    email, password = data["email"], data["password"]
    response = verify_user(email, password)
    if response["success"]:
        return jsonify({"message": response["message"], "access_token": str(response['token'])})
    return jsonify({"error": response["message"]}), 401
