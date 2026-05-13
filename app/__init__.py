from flask import Flask
from app.extensions import db, socketio, migrate
from config import Config

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

# initialisation of app
    db.init_app(app)
    migrate.init_app(app,db)
    socketio.init_app(app, cors_allowed_origins="*")

    from app.routes import rooms_bp
    app.register_blueprint(rooms_bp)

    from app import events

    return app