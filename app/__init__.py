from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .models import db
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    from .routes.auth import auth_bp
    from .routes.posts import posts_bp
    from .routes.users import users_bp
    from .routes.comments import comments_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(posts_bp, url_prefix="/posts")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(comments_bp, url_prefix="/comments")
    
    return app