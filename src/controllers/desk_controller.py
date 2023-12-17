from flask import Blueprint, request
from app import db
from auth import authorise
from models.desk import *
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError
from marshmallow.exceptions import ValidationError

# desk route url is defined as an instance of Blueprint which is registered in __init__.py
desk = Blueprint("desk", __name__, url_prefix="/desk")


# ALL DESK ROUTES ARE ACCESSIBLE BY ADMIN ONLY

# The GET route endpoint (show all)
@jwt_required()
@desk.route("/")
def get_desks():
    authorise(None, True)
    # Retrieves all desks using the select function to select Desk class
    db_desks = db.select(Desk)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    desks = db.session.scalars(db_desks)

    # The DeskSchema and dump() method serialises the data and returns the formatted result
    return DeskSchema(many=True).dump(desks), 200


# The GET route endpoint (show desk)
@jwt_required()
@desk.route("/<string:id>")
def get_desk(id):
    authorise(None, True)
    # Retrieves desk with id specified in the URL using the select function to select Desk class
    stmt = db.select(Desk).filter_by(id=id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    desk = db.session.scalar(stmt)

    if desk:
        # The DeskSchema and dump() method serialises the data and returns the formatted result
        return DeskSchema().dump(desk), 200
    else:
        return {"message" : "desk not found"}, 404



# The POST route endpoint (create new)
@jwt_required()
@desk.route("/", methods=["POST"])
def create_desk():
    authorise(None, True)
    try:
        try:
            # Receives JSON data via the HTTP request which is deserialised using the load() method
            new_desk = DeskSchema().load(request.json)
        except ValidationError:
            return {"message" : "Ensure desk_id has been entered"}

        desk = Desk(
            id = new_desk["id"],
            available = new_desk["available"]
        )
        # Adds the new desk to the database (equivalent of SQL INSERT)
        db.session.add(desk)
        # Closes the session and commits the current transaction
        db.session.commit()
        # The DeskSchema and dump() method serialises the data and returns the formatted result
        return DeskSchema().dump(desk), 201
    except (IntegrityError, KeyError, DataError):
        return {"error" : "Check if new desk id entered already exists"}, 409





# The PUT route endpoint (edit desk)
@jwt_required()
@desk.route("/<string:id>", methods=["PUT", "PATCH"])
def edit_desk(id):
    authorise(None, True)
    try:
        # Receives JSON data via the HTTP request which is deserialised using the load() method
        update_desk = DeskSchema().load(request.json)
    except ValidationError:
        return {"message" : "Ensure desk_id has been entered"}
    # Retrieves desk with id specified in the URL using the select function to select Desk class
    stmt = db.select(Desk).filter_by(id=id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)    
    desk = db.session.scalar(stmt)

    try:
        if desk: # Only executes if a desk was found in the filter
            # Changes each of the desk's attributes if a new value was parsed
            # If not, the attribute will remain as it was
            desk.id = update_desk.get("id", desk.id)
            desk.available = update_desk.get("available", desk.available)
            # Once the desk object has been updated it can be committed to the database
            db.session.commit()
            # The DeskSchema and dump() method serialises the data and returns the formatted result
            return DeskSchema().dump(desk), 200
        else:
            return {"message" : "desk not found"}, 404
    except (IntegrityError, KeyError, DataError):
        return {"error" : "Check if new desk id entered already exists"}, 409


# The DELETE route endpoint (delete existing)
@jwt_required()
@desk.route("/<string:id>", methods=["DELETE"])
def delete_desk(id):
    authorise(None, True)
    # Retrieves desk with id specified in the URL using the select function to select Desk class
    stmt = db.select(Desk).filter_by(id=id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    desk = db.session.scalar(stmt)

    if desk: # If statement is only executed if a matching desk was found
        try:
            # Uses the current session to remove the desk from the database
            db.session.delete(desk)
            # Closes the session and commits the current transaction
            db.session.commit()
            return {}, 200
        except IntegrityError:
            return {"message" : "There are bookings associated with this desk, therefore it cannot be deleted"}, 405
    else:
        return {"message" : "desk not found"}, 404

