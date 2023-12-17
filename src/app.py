from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# app.py creates objects of SQLAlchemy (the ORM),
# Marshmallow (object serialisation/deserialisation),
# Bcrypt (password encyrption) & JWT (handles JSON web tokens)

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    # A Flask app is created
    app = Flask(__name__)

    app.config.from_object('config.app_config')

    # The SQLAlchemy object is initialised with the app
    # followed by the marshmallow, bcrypt and JWT objects
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # The blueprints are registered with the app
    from db_setup import db_commands
    app.register_blueprint(db_commands)

    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)

    
    print(app.url_map)

    return app



