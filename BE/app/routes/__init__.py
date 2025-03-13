# Blueprint 등록

from routes.auth_routes import auth_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
