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
    # Retrieves all depts using the select function to select Dept class
    db_depts = db.select(Dept)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    depts = db.session.scalars(db_depts).all()
    # The DeptSchema and dump() method serialises the data and returns the formatted result
    return DeptSchema(many=True).dump(depts), 200


# The POST route endpoint (create new)
@jwt_required()
@dept.route("/", methods=["POST"])
def add_dept():
    authorise(None, True)
    # Receives JSON data via the HTTP request which is deserialised using the load() method
    new_dept = DeptSchema().load(request.json)

    dept = Dept(
        name = new_dept["name"]
    )
    # Adds the new dept to the database (equivalent of SQL INSERT)
    db.session.add(dept)
    # Closes the session and commits the current transaction
    db.session.commit()

    # The DeptSchema and dump() method serialises the data and returns the formatted result
    return DeptSchema().dump(dept), 201


# The PUT route endpoint (edit existing)
@jwt_required()
@dept.route("/<int:id>", methods=["PUT", "PATCH"])
def update_dept(id):
    try:
        # Receives JSON data via the HTTP request which is deserialised using the load() method
        update_info = DeptSchema().load(request.json)
    except ValidationError:
        return {"message" : "Ensure department name has been entered"}
    if len(update_info) > 0:
        # Retrieves dept with id specified in the URL using the select function to select Dept class
        stmt = db.select(Dept).filter_by(id=id)
        # The session object creates a session related to the Flask app
        # scalars returns single elements of the database row(s)
        dept = db.session.scalar(stmt)

        if dept: # Only executes if a dept was found in the filter
            authorise(None, True)
            # Dept only has one attribute, so this is updated according to the HTTP request
            # If no dept name was entered, it will remain as it was
            dept.name = update_info.get("name", dept.name)

            # Closes the session and commits the current transaction
            db.session.commit()
        # The DeptSchema and dump() method serialises the data and returns the formatted result
            return DeptSchema().dump(dept), 200
        else:
            return {"message" : "department not found"}, 404
    else:
        return {"message" : "Dept not updated as no details were entered"}





# The DELETE route endpoint (delete existing)
@jwt_required()
@dept.route("/<int:id>", methods=["DELETE"])
def delete_dept(id):
    # Retrieves dept with id specified in the URL using the select function to select Dept class
    stmt = db.select(Dept).filter_by(id=id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    dept = db.session.scalar(stmt)

    if dept: # Only executes if a dept was found in the filter
        authorise(None, True)
        # Uses the current session to remove the dept from the database
        db.session.delete(dept)
        # Closes the session and commits the current transaction
        db.session.commit()
        return {}, 200
    else:
        return {"message" : "department not found"}, 404
