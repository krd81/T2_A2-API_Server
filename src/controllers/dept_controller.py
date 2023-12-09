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


# ALL DEPARTMENT ACTIONS NEED TO BE RESTRICTED TO ADMIN ONLY
dept = Blueprint('dept', __name__, url_prefix='/dept')
unauthorised_user

# The GET route endpoint (show all)
@dept.route('/')
def show_depts():
    db_depts = db.select(Dept)
    depts = db.session.scalars(db_depts).all()
    return DeptSchema(many=True).dump(depts), 200


# The POST route endpoint (create new)
@dept.route('/', methods=['POST'])
def add_dept():
    new_dept = NewDeptSchema().load(request.json)

    dept = Dept(
        name = new_dept["name"]
    )

    db.session.add(dept)
    db.session.commit()

    return NewDeptSchema().dump(dept), 201


# The PUT route endpoint (edit existing)
@dept.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_dept(id):
    update_info = NewDeptSchema().load(request.json)
    stmt = db.select(Dept).filter_by(id=id)
    dept = db.session.scalar(stmt)

    if dept:
        dept.name = update_info.get("name", dept.name)

        db.session.commit()
        return NewDeptSchema().dump(dept), 200
    else:
        return {'message' : 'department not found - please try again'}, 404




# The DELETE route endpoint (delete existing)
@dept.route('/<int:id>', methods=['DELETE'])
def delete_dept(id):
    # delete_dept = DeptSchema().load(request.json)
    stmt = db.select(Dept).filter_by(id=id)
    dept = db.session.scalar(stmt)

    if dept:
        db.session.delete(dept)
        db.session.commit()
        return {}, 200
    else:
        return {'message' : 'department not found - please try again'}, 404





# return {'message' : 'obj not found - please try again'}, 404
# return .dump(obj), 200