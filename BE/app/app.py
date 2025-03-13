# Flask 앱 실행

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import send_from_directory
from routes.auth_routes import auth_bp
from routes.todo_routes import todo_bp
# from models import db
# from routes import register_routes
# import config


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"  # 시크릿 키 설정
jwt = JWTManager(app)

# 데이터베이스 마이그레이션
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "supersecretkey"

db = SQLAlchemy(app)
migrate = Migrate(app, db) # Flask-Migrate 초기화

# # 설정 파일 로드
# app.config.from_object(config)

# # 데이터베이스 초기화
# db.init_app(app)

# 라우트 등록
# register_routes(app)

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(todo_bp, url_prefix="/api")

@app.route("/")
def home():
    return "메인 페이지"

@app.route("/login")
def serve_login():
    return send_from_directory("static", "index.html")

@app.route("/todo")
def serve_todo():
    return send_from_directory("static", "todo.html")

if __name__ == "__main__":
    app.run(debug=True)