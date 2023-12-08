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
@user.route('/')
def get_users():
    pass

# The GET route endpoint (show all)
@user.route('/<int:id>')
def get_user(id):
    pass



# The POST route endpoint (create new)
@user.route('/', methods=['POST'])
def CREATE():
    pass


# The PUT route endpoint (edit existing)
@user.route('/<int:id>', methods=['PUT', 'PATCH'])
def change_password(id):
    pass


# The DELETE route endpoint (delete existing)
@user.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    pass


# return {'message' : 'obj not found - please try again'}, 404
# return .dump(obj), 200