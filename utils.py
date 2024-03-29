from flask import Flask
from models import db
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')

    return app


def init_app(app):
    db.init_app(app)
    Migrate(app, db)