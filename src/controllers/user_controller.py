from flask import Blueprint, request
from app import db, bcrypt
from controllers.booking_controller import booking
from models.user import *
from auth import authorise
from flask_jwt_extended import jwt_required, create_access_token
from sqlalchemy.exc import IntegrityError, DataError
from marshmallow.exceptions import ValidationError
from datetime import timedelta

# user route url is defined as an instance of Blueprint which is registered in __init__.py
user = Blueprint("user", __name__, url_prefix="/user")
# booking blueprint registered here as its path is via 'user'
user.register_blueprint(booking)

# user_controller contains functions that general users are able to do 
# (i.e. login, view their details, change password)
# Note - admins can access ALL routes



# The GET route endpoint (show user)
# Can only see themselves (Admin can see all)
@jwt_required()
@user.route("/<string:id>")
def get_user(id):
    try:
        # Retrieves user with id specified in the URL using the select function to select User class
        stmt = db.select(User).filter_by(employee_id=id)
        # The session object creates a session related to the Flask app
        # scalars returns single elements of the database row(s)
        user = db.session.scalar(stmt)
        # Only executes if a user was found in the filter
        if user: 
            authorise(user.id)
            # The UserSchema and dump() method serialises the data and returns the formatted result, excluding "password" and "is_admin"
            return UserSchema(exclude=["password", "is_admin"]).dump(user), 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "user not found"}, 404




# The POST route endpoint (user login)
@user.route("/", methods=["POST"])
def signin():
    try:
        # Receives JSON data via the HTTP request which is deserialised using the load() method
        current_user = UserSchema().load(request.json)
    except ValidationError:
        return {"message" : "Ensure employee id and password has been entered"}, 400

    # Retrieves all users matching the filter (i.e. employee id in database matches the id supplied) 
    # using the select function to select User class
    stmt = db.select(User).filter_by(employee_id=current_user["employee_id"])
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    user = db.session.scalar(stmt)

    try:
        # Only executes if a user was found in the filter and their password matches the user's (hashed) password
        if user and bcrypt.check_password_hash(user.password, current_user["password"]):
            token = create_access_token(identity=user.id, additional_claims={"id": user.id}, expires_delta = timedelta(hours = 100))
            # The UserSchema and dump() method serialises the data and returns the formatted result, excluding "password" and "is_admin"
            return {"token" : token, "user" : UserSchema(exclude=["password", "is_admin"]).dump(user)}, 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"error" : "Employee id or password is incorrect"}, 409



# The PUT route endpoint (edit existing user: PASSWORD ONLY)
@user.route("/<string:id>", methods=["PUT", "PATCH"])
@jwt_required()
def change_password(id):
    try:
        # Receives JSON data via the HTTP request which is deserialised using the load() method
        update_user = UserSchemaPassword().load(request.json)
        # Retrieves user with id specified in the URL using the select function to select User class
        stmt = db.select(User).filter_by(employee_id=id)
        # The session object creates a session related to the Flask app
        # scalars returns single elements of the database row(s)
        user = db.session.scalar(stmt)
    except ValidationError:
        return {"message" : "Ensure a new password, between 8 and 12 characters has been entered"}, 400

    try:
        if user: # Only executes if a user was found in the filter
            authorise(user.id)
            # Password is the only field that will be accepted
            # If no password was retrieved, it will remain the same
            user.password = bcrypt.generate_password_hash(update_user.get("password", user.password)).decode("utf8")
            # Once the password has been updated it can be committed to the database
            db.session.commit()
            # The UserSchema and dump() method serialises the data and returns the formatted result, excluding "password" and "is_admin"
            return UserSchema(exclude=["password", "is_admin"]).dump(user), 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "User not found"}, 404

