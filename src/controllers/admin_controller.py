from flask import Blueprint, request
from app import db, bcrypt
from auth import authorise
from models.user import *
from flask_jwt_extended import jwt_required, create_access_token
from sqlalchemy.exc import IntegrityError, DataError
from marshmallow.exceptions import ValidationError
from datetime import timedelta

# admin route url is defined as an instance of Blueprint which is registered in __init__.py
admin = Blueprint("admin", __name__, url_prefix="/admin")


# ADMIN ONLY ROUTES: controls creating users / editing user details / deleting users
# View all users is an admin only function, so exists here, not in user_controller

# Get all users (GET method)
@jwt_required()
@admin.route("/")
def get_users():
    authorise(None, True)
    # Retrieves all users using the select function to select User class
    db_users = db.select(User)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    users = db.session.scalars(db_users).all()
    # The UserSchema and dump() method serialises the data and returns the formatted result, excluding "password"
    return UserSchema(exclude=["password"], many=True).dump(users), 200



# Create new users (POST)
@jwt_required()
@admin.route("/", methods = ["POST"])
def create_user():
    try:
        authorise(None, True)
        try:
            # Receives JSON data via the HTTP request which is deserialised using the load() method
            new_user = CreateUserSchema().load(request.json)
        except ValidationError:
            return {"message" : "Ensure all User fields are present (password must be between 8 and 14 characters)"}, 400
        # Create new user
        user = User(
            employee_id = new_user["employee_id"],
            f_name = new_user["f_name"],
            l_name = new_user["l_name"],
            email = new_user["email"],
            password = bcrypt.generate_password_hash(new_user["password"]).decode("utf8"),
            dept_id = new_user["dept_id"]
        )

        # Add and commit the new user to the database (equivalent of SQL INSERT)
        db.session.add(user)
        db.session.commit()


        # Return JWT / user
        # The UserSchema and dump() method serialises the data and returns the formatted result, excluding "password"
        return UserSchema(exclude=["password"]).dump(user), 201
    except (IntegrityError, KeyError, DataError):
        return {"error" : "Either employee id is already registered or there is an error with the department"}, 409


# The PUT route endpoint (edit user details)
@jwt_required()
@admin.route("/<string:id>", methods=["PUT", "PATCH"])
def edit_user(id):
    authorise(None, True)
    try:
        # Receives JSON data via the HTTP request which is deserialised using the load() method
        update_user = UserSchema().load(request.json)
    except ValidationError:
        return {"message" : "Ensure email/password fields, if entered, contain valid data)"}, 400
    if len(update_user) > 0:
        # Retrieves all users matching the filter using the select function to select User class
        stmt = db.select(User).filter_by(employee_id=id)
        # The session object creates a session related to the Flask app
        # scalars returns single elements of the database row(s)
        user = db.session.scalar(stmt)

        try:
            if user: # Only executes if a user was found in the filter
                # Changes each of the user's attributes if a new value was parsed
                # If not, the attribute will remain as it was
                user.employee_id = update_user.get("employee_id", user.employee_id)
                user.f_name = update_user.get("f_name", user.f_name)
                user.l_name = update_user.get("l_name", user.l_name)
                user.email = update_user.get("email", user.email)
                user.password = update_user.get("password", user.password)
                user.dept_id = update_user.get("dept_id", user.dept_id)
                user.is_admin = update_user.get("is_admin", user.is_admin)

                # Once the user object has been updated it can be committed to the database
                db.session.commit()
                # The UserSchema and dump() method serialises the data and returns the formatted result, excluding "password"
                return UserSchema(exclude=["password"]).dump(user), 200
            else:
                return {"message" : "user not found"}, 404
        except (IntegrityError, KeyError, DataError):
            return {"error" : "Either employee id is already registered or there is an error with the department"}, 409
    else:
        return {"message" : "User not updated as no details were entered"}



# The DELETE route endpoint (delete user)
@jwt_required()
@admin.route("/<string:id>", methods=["DELETE"])
def delete_user(id):
    # Retrieves all users matching the filter using the select function to select User class
    stmt = db.select(User).filter_by(employee_id=id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    user = db.session.scalar(stmt)

    if user: # If statement is only executed if a matching user was found
        authorise(None, True)
        # Uses the current session to remove the user from the database
        db.session.delete(user)
        # Closes the session and commits the current transaction
        db.session.commit()

        return {}, 200
    else:
        return {"message" : "user not found"}, 404
