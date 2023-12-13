from flask import Blueprint, request
from app import db, bcrypt
from auth import authorise
from models.user import *
from flask_jwt_extended import jwt_required, create_access_token
from sqlalchemy.exc import IntegrityError, DataError
from marshmallow.exceptions import ValidationError
from datetime import timedelta


admin = Blueprint("admin", __name__, url_prefix="/admin")
# unauthorised_user

# ADMIN ONLY ROUTES: controls creating users / editing user details / deleting users

@jwt_required()
@admin.route("/", methods = ["POST"])
def create_user():
    try:
        authorise(None, True)
        try:
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

        # Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=user.id, additional_claims={"id": user.id}, expires_delta = timedelta(hours = 100))
        # Return JWT / user   
        return {"token" : token, "user" : UserSchema(exclude=["password", "is_admin"]).dump(user)}, 201
    except (IntegrityError, KeyError, DataError):
        return {"error" : "Either employee id is already registered or there is an error with the department"}, 409
    

# The PUT route endpoint (edit user details)
@jwt_required()
@admin.route("/<string:id>", methods=["PUT", "PATCH"])
def edit_user(id):
    try:
        update_user = UserSchema().load(request.json)
    except ValidationError:
        return {"message" : "Ensure email/password fields, if entered, contain valid data)"}, 400
    if len(update_user) > 0:
        stmt = db.select(User).filter_by(employee_id=id)
        user = db.session.scalar(stmt)

        try:
            if user:
                authorise(None, True)
                user.employee_id = update_user.get("employee_id", user.employee_id)
                user.f_name = update_user.get("f_name", user.f_name)
                user.l_name = update_user.get("l_name", user.l_name)
                user.email = update_user.get("email", user.email)
                user.password = update_user.get("password", user.password)
                user.dept_id = update_user.get("dept_id", user.dept_id)   
                user.is_admin = update_user.get("is_admin", user.is_admin)     
                
                db.session.commit()

                return UserSchema(exclude=["password"]).dump(user), 200
            else:
                return {"message" : "user not found - please try again"}, 404
        except (IntegrityError, KeyError, DataError):
            return {"error" : "Either employee id is already registered or there is an error with the department"}, 409
    else:
        return {"message" : "User not updated as no details were entered"}



# The DELETE route endpoint (delete user)
@jwt_required()
@admin.route("/<string:id>", methods=["DELETE"])
def delete_user(id):
    stmt = db.select(User).filter_by(employee_id=id)
    user = db.session.scalar(stmt)

    if user:
         authorise(None, True)
         db.session.delete(user)
         db.session.commit()

         return {}, 200
    else:
        return {"message" : "user not found - please try again"}, 404
