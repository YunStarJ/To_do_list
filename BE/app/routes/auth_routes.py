# 로그인, 회원가입 API

from flask import Blueprint, request, jsonify
from models.user import User
from models import db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = generate_password_hash(data["password"])

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "동일한 아이디가 존재합니다."}), 400

    return jsonify({"message": "회원가입이 완료되었습니다."}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"message": "인증 실패"}), 401
