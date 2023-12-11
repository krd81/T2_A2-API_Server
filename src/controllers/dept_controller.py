from flask import Blueprint, request
from app import db, unauthorised_user, bcrypt
from auth import authorise
# from models.booking import *
# from models.booking_date import *
from models.dept import *
# from models.desk import *
# from models.user import *
from flask_jwt_extended import jwt_required, create_access_token
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta

# ADMIN ONLY FUNCTIONS

dept = Blueprint('dept', __name__, url_prefix='/dept')
unauthorised_user

# The GET route endpoint (show all)
@jwt_required()
@dept.route('/')
def show_depts():
    authorise()
    db_depts = db.select(Dept)
    depts = db.session.scalars(db_depts).all()
    return DeptSchema(many=True).dump(depts), 200


# The POST route endpoint (create new)
@jwt_required()
@dept.route('/', methods=['POST'])
def add_dept():
    authorise()
    new_dept = NewDeptSchema().load(request.json)

    dept = Dept(
        name = new_dept["name"]
    )

    db.session.add(dept)
    db.session.commit()

    return NewDeptSchema().dump(dept), 201


# The PUT route endpoint (edit existing)
@jwt_required()
@dept.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_dept(id):
    update_info = NewDeptSchema().load(request.json)
    stmt = db.select(Dept).filter_by(id=id)
    dept = db.session.scalar(stmt)

    if dept:
        authorise()
        dept.name = update_info.get("name", dept.name)

        db.session.commit()
        return NewDeptSchema().dump(dept), 200
    else:
        return {'message' : 'department not found - please try again'}, 404




# The DELETE route endpoint (delete existing)
@jwt_required()
@dept.route('/<int:id>', methods=['DELETE'])
def delete_dept(id):
    stmt = db.select(Dept).filter_by(id=id)
    dept = db.session.scalar(stmt)

    if dept:
        authorise()
        db.session.delete(dept)
        db.session.commit()
        return {}, 200
    else:
        return {'message' : 'department not found - please try again'}, 404
