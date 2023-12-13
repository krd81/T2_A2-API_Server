from flask import Blueprint, request
from app import db
from auth import authorise
from models.desk import *
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError
from marshmallow.exceptions import ValidationError



desk = Blueprint("desk", __name__, url_prefix="/desk")


# ALL DESK ROUTES ARE ACCESSIBLE BY ADMIN ONLY

# The GET route endpoint (show all)
@jwt_required()
@desk.route("/")
def get_desks():
    authorise(None, True)
    db_desks = db.select(Desk)
    desks = db.session.scalars(db_desks)

    return DeskSchema(many=True).dump(desks), 200


# The GET route endpoint (show desk)
@jwt_required()
@desk.route("/<string:id>")
def get_desk(id):
    authorise(None, True)
    stmt = db.select(Desk).filter_by(id=id)
    desk = db.session.scalar(stmt)

    if desk:
        return DeskSchema().dump(desk), 200
    else:
        return {"message" : "desk not found - please try again"}, 404



# The POST route endpoint (create new)
@jwt_required()
@desk.route("/", methods=["POST"])
def create_desk():
    authorise(None, True)
    try:
        try:
            new_desk = DeskSchema().load(request.json)
        except ValidationError:
            return {"message" : "Ensure desk_id has been entered"}

        desk = Desk(
            id = new_desk["id"],
            available = new_desk["available"]
        )

        db.session.add(desk)
        db.session.commit()
        return DeskSchema().dump(desk), 201
    except (IntegrityError, KeyError, DataError):
        return {"error" : "Check if new desk id entered already exists"}, 409





# The PUT route endpoint (edit desk)
@jwt_required()
@desk.route("/<string:id>", methods=["PUT", "PATCH"])
def edit_desk(id):
    authorise(None, True)
    try:
        update_desk = DeskSchema().load(request.json)
    except ValidationError:
        return {"message" : "Ensure desk_id has been entered"}
    stmt = db.select(Desk).filter_by(id=id)
    desk = db.session.scalar(stmt)

    try:
        if desk:
            desk.id = update_desk.get("id", desk.id)
            desk.available = update_desk.get("available", desk.available)
            db.session.commit()
            return DeskSchema().dump(desk), 200
        else:
            return {"message" : "desk not found - please try again"}, 404
    except (IntegrityError, KeyError, DataError):
        return {"error" : "Check if new desk id entered already exists"}, 409


# The DELETE route endpoint (delete existing)
@jwt_required()
@desk.route("/<string:id>", methods=["DELETE"])
def delete_desk(id):
    authorise(None, True)

    stmt = db.select(Desk).filter_by(id=id)
    desk = db.session.scalar(stmt)

    if desk:
        try:
            db.session.delete(desk)
            db.session.commit()
            return {}, 200
        except IntegrityError:
            return {"message" : "There are bookings associated with this desk, therefore it cannot be deleted"}, 405
    else:
        return {"message" : "desk not found - please try again"}, 404


'''
def get_desk(desk_id=None , activity=""):
    authorise(None, True)
    desk_info = DeskSchema().load(request.json)

    if not desk_id == None :
        stmt = db.select(Desk).filter_by(id=desk_id)
        desk = db.session.scalar(stmt)
        if desk:
            if activity == "delete":
                return desk
            elif activity == "update":
                desk.id = desk_info.get("id", desk.id)
                desk.available = desk_info.get("available", desk.available)
                return desk
    else:
        if activity == "create":
            new_desk = Desk(
                id = desk_info["id"],
                available = desk_info["available"]
            )
            return new_desk
'''





