# 사용자 모델 데이터베이스 테이블

from flask_sqlalchemy import SQLAlchemy
from models import db

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)