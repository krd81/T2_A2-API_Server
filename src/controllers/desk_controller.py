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


desk = Blueprint('desk', __name__, url_prefix='/desk')
unauthorised_user

# The GET route endpoint (show all)
@desk.route('/')
def get_desks():
    pass

# The GET route endpoint (show all)
@desk.route('/<int:id>')
def get_desk(id):
    pass



# The POST route endpoint (create new)
@desk.route('/', methods=['POST'])
def add_desk():
    pass


# The PUT route endpoint (edit existing)
@desk.route('/<int:id>', methods=['PUT', 'PATCH'])
def EDIT(id):
    pass


# The DELETE route endpoint (delete existing)
@desk.route('/<int:id>', methods=['DELETE'])
def delete_desk(id):
    pass


# return {'message' : 'obj not found - please try again'}, 404
# return .dump(obj), 200