from flask import Blueprint, request
from app import db
from auth import authorise
from models.dept import *
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError



# ADMIN ONLY FUNCTIONS

dept = Blueprint("dept", __name__, url_prefix="/dept")
# unauthorised_user


# The GET route endpoint (show all)
@jwt_required()
@dept.route("/")
def show_depts():
    authorise(None, True)
    db_depts = db.select(Dept)
    depts = db.session.scalars(db_depts).all()
    return DeptSchema(many=True).dump(depts), 200


# The POST route endpoint (create new)
@jwt_required()
@dept.route("/", methods=["POST"])
def add_dept():
    authorise(None, True)
    new_dept = DeptSchema().load(request.json)

    dept = Dept(
        name = new_dept["name"]
    )

    db.session.add(dept)
    db.session.commit()

    return DeptSchema().dump(dept), 201


# The PUT route endpoint (edit existing)
@jwt_required()
@dept.route("/<int:id>", methods=["PUT", "PATCH"])
def update_dept(id):
    try:
        update_info = DeptSchema().load(request.json)
    except ValidationError:
        return {"message" : "Ensure department name has been entered"}
    if len(update_info) > 0:
        stmt = db.select(Dept).filter_by(id=id)
        dept = db.session.scalar(stmt)

        if dept:
            authorise(None, True)
            dept.name = update_info.get("name", dept.name)

            db.session.commit()
            return DeptSchema().dump(dept), 200
        else:
            return {"message" : "department not found"}, 404
    else:
        return {"message" : "Dept not updated as no details were entered"}





# The DELETE route endpoint (delete existing)
@jwt_required()
@dept.route("/<int:id>", methods=["DELETE"])
def delete_dept(id):
    stmt = db.select(Dept).filter_by(id=id)
    dept = db.session.scalar(stmt)

    if dept:
        authorise(None, True)
        db.session.delete(dept)
        db.session.commit()
        return {}, 200
    else:
        return {"message" : "department not found"}, 404
