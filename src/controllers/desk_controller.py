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

# ADMIN ONLY?

# The GET route endpoint (show all)
@desk.route('/')
def get_desks():
    db_desks = db.select(Desk)
    desks = db.session.scalars(db_desks)

    return DeskSchema(many=True).dump(desks), 200


# The GET route endpoint (show desk)
@desk.route('/<string:id>')
def get_desk(id):
    stmt = db.select(Desk).filter_by(id=id)
    desk = db.session.scalar(stmt)

    if desk:
        return DeskSchema().dump(desk), 200        
    else:
        return {'message' : 'desk not found - please try again'}, 404



# The POST route endpoint (create new)
@desk.route('/', methods=['POST'])
def add_desk():
    new_desk = DeskSchema().load(request.json)

    desk = Desk(
        id = new_desk["id"]
    )

    db.session.add(desk)
    db.session.commit()
    return DeskSchema().dump(desk), 201



# The PUT route endpoint (edit desk)
@desk.route('/<string:id>', methods=['PUT', 'PATCH'])
def EDIT(id):
    update_desk = DeskSchema().load(request.json)
    stmt = db.select(Desk).filter_by(id=id)
    desk = db.session.scalar(stmt)

    if desk:
        desk.id = update_desk.get("id", desk.id)
        desk.available = update_desk.get("available", desk.available)
        db.session.commit()
        return DeskSchema().dump(desk), 200
    else:
        return {'message' : 'desk not found - please try again'}, 404


# The DELETE route endpoint (delete existing)
@desk.route('/<string:id>', methods=['DELETE'])
def delete_desk(id):
    stmt = db.select(Desk).filter_by(id=id)
    desk = db.session.scalar(stmt)

    if desk:
        db.session.delete(desk)
        db.session.commit()
        return {}, 200
    else:
        return {'message' : 'desk not found - please try again'}, 404



