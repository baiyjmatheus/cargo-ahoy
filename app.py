from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_json_schema import JsonSchema
from config import get_config

db = SQLAlchemy()
schema = JsonSchema()


def create_app(env=None):
    app = Flask(__name__)
    app.config.from_object(get_config(env))
    db.init_app(app)
    schema.init_app(app)
    return app
