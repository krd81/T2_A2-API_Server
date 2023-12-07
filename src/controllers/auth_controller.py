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


auth = Blueprint('auth', __name__, url_prefix='/auth')
unauthorised_user

# Signup/Register: POST route endpoint
# ADMIN ONLY ROUTE
@auth.route('/signup', methods = ['POST'])
def signup():
    # try:
        current_user = UserSchema().load(request.json)                  
        # Create new user
        user = User(
            id = current_user['id'],
            f_name = current_user['f_name'],
            l_name = current_user['l_name'],
            email = current_user['email'],
            password = bcrypt.generate_password_hash(current_user['password']).decode('utf8'),
            dept_id = current_user['dept_id']
        )
        # Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=user.id, additional_claims={'id': user.id}, expires_delta = timedelta(hours = 100))
        # Return JWT / user   
        return {'token' : token, 'user' : UserSchema(exclude=['password', 'is_admin']).dump(user)}, 201
    # except IntegrityError:
        # return {'error' : 'Another user has already registered that username'}, 409
    

# Signin / Login: POST route endpoint
@auth.route('/signin', methods = ['POST'])
def signin():
    current_user = UserSchema().load(request.json)

    stmt = db.select(User).filter_by(id=current_user['id'])
    user = db.session.scalar(stmt)

    if user and bcrypt.check_password_hash(user.password, current_user['password']):
        token = create_access_token(identity=user.id, additional_claims={'id': user.id}, expires_delta = timedelta(hours = 100))
        return {'token' : token, 'user' : UserSchema(exclude=['id', 'is_admin']).dump(user)}, 200
    else:
        return {'error' : 'Username or password is incorrect'}, 409
