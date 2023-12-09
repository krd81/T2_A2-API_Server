from flask import Blueprint, request
from app import db, unauthorised_user, bcrypt
from models.booking import *
from models.booking_date import *
from models.dept import *
from models.desk import *
from models.user import *
from flask_jwt_extended import jwt_required, create_access_token
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta


user = Blueprint('user', __name__, url_prefix='/user')
unauthorised_user

# The GET route endpoint (show all)
# ADMIN ONLY
@user.route('/')
def get_users():
    db_users = db.select(User)
    users = db.session.scalars(db_users).all()
    return UserSchema(exclude=["password"], many=True).dump(users), 200


# The GET route endpoint (show user)
# Can only see themselves (Admin can see all)
@user.route('/<string:id>')
def get_user(id):
    stmt = db.select(User).filter_by(employee_id=id)
    user = db.session.scalar(stmt)

    if user:
        return UserSchema(exclude=["password"]).dump(user), 200
    else:
        return {'message' : 'user not found - please try again'}, 404




# The POST route endpoint (user login)
@user.route('/', methods=['POST'])
def signin():
    current_user = UserSchema().load(request.json)

    stmt = db.select(User).filter_by(employee_id=current_user['employee_id'])
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, current_user['password']):
        token = create_access_token(identity=user.id, additional_claims={'id': user.id}, expires_delta = timedelta(hours = 100))
        return {'token' : token, 'user' : UserSchema(exclude=['password', 'is_admin']).dump(user)}, 201
    else:
        return {'error' : 'Username or password is incorrect'}, 409



# The PUT route endpoint (edit existing user: PASSWORD ONLY)
@user.route('/<string:id>', methods=['PUT', 'PATCH'])
def change_password(id):
    update_user = UserSchema().load(request.json)
    stmt = db.select(User).filter_by(employee_id=id)
    user = db.session.scalar(stmt)

    if user:
        # bcrypt.generate_password_hash(new_user["password"]).decode("utf8")
        user.password = bcrypt.generate_password_hash(update_user.get("password", user.password)).decode("utf8")
        db.session.commit()
        return UserSchema(exclude=["password"]).dump(user), 200
    else:
        return {'message' : 'user not found - please try again'}, 404

