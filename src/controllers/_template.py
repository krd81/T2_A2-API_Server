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


contoller_name = Blueprint('temp', __name__, url_prefix='/temp')
unauthorised_user

# The GET route endpoint (show all)
@temp.route('/')
def GET_ALL_ROUTE():
    pass

# The GET route endpoint (show all)
@temp.route('/<int:id>')
def GET_ONE_ROUTE():
    pass



# The POST route endpoint (create new)
@temp.route('/', methods=['POST'])
def CREATE():
    pass


# The PUT route endpoint (edit existing)
@temp.route('/<int:id>', methods=['PUT', 'PATCH'])
def EDIT():
    pass


# The DELETE route endpoint (delete existing)
@temp.route('/<int:id>', methods=['DELETE'])
def DELETE():
    pass


# return {'message' : 'obj not found - please try again'}, 404
# return .dump(obj), 200