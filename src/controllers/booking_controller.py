from flask import Blueprint, request
from app import db
from auth import authorise
from models.booking import *
from models.user import *
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError
from marshmallow.exceptions import ValidationError


# Some routes (ie: create new, edit, delete need to be accessed via the user controller)
# Booking needs a checking mechanism to ensure the desk is available


booking = Blueprint("booking", __name__, url_prefix="/<string:employee_id>/booking")



# The GET route endpoint (show all for individual user)
@jwt_required()
@booking.route("/")
def get_bookings(employee_id):
    stmt = db.select(User).filter_by(employee_id=employee_id)
    user = db.session.scalar(stmt)

    try:
        authorise(user.id)

        stmt = db.select(Booking).filter_by(user_id=employee_id)
        bookings = db.session.scalars(stmt)

        return BookingSchema(many=True).dump(bookings), 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "User not found"}, 400


# The GET route endpoint (show booking)
@jwt_required()
@booking.route("/<int:id>") # /booking/booking_id [GET]
def get_booking(employee_id, id):
    stmt = db.select(User).filter_by(employee_id=employee_id)
    user = db.session.scalar(stmt)

    try:
        if user:
            authorise(user.id)
            stmt = db.select(Booking).filter_by(user_id=employee_id, id=id)
            booking = db.session.scalar(stmt)

            if booking:
                return BookingSchema().dump(booking), 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "User and/or booking not found"}, 400


# The POST route endpoint (create new)
@jwt_required()
@booking.route("/", methods=["POST"]) # /user_id/booking [POST]
def new_booking(employee_id):
    stmt = db.select(User).filter_by(employee_id=employee_id)
    user = db.session.scalar(stmt)

    if user:
        authorise(user.id)
        try:
            new_booking = BookingSchema().load(request.json)
        except ValidationError:
            return {"message" : "Weekday must be one of 'mon', 'tue', 'wed', 'thu', 'fri'"}, 400

        booking = Booking (
            weekday = new_booking["weekday"],
            desk_id = new_booking["desk_id"],
            user_id = employee_id,
            week_id = new_booking["week_id"]
        )

        stmt = db.select(Booking).filter_by(booking_ref=booking.get_booking_ref(booking.desk_id, booking.week_id, booking.weekday))
        conflicting_booking = db.session.scalar(stmt)
        try:
            if not conflicting_booking or booking.desk_id.available:
                db.session.add(booking)
                db.session.commit()

                return BookingSchema().dump(booking), 201
            else:
                return {"message" : "Desk is unavailable - please try again"}, 409
        except (IntegrityError, DataError):
            return {"message" : "Invalid input - please check and try again"}, 400
    else:
        return {"message" : "You are not authorised to access this resource"}, 401




# The PUT route endpoint (edit existing) # /user_id/booking/booking_id [PUT]
@jwt_required()
@booking.route("/<int:id>", methods=["PUT", "PATCH"])
def edit_booking(employee_id, id):
    stmt = db.select(User).filter_by(employee_id=employee_id)
    user = db.session.scalar(stmt)

    if user:
        authorise(user.id)

        try:
            update_booking = BookingSchema().load(request.json)
        except ValidationError:
            return {"message" : "Check booking details entered"}

        stmt = db.select(Booking).filter_by(user_id=employee_id, id=id)
        booking = db.session.scalar(stmt)

        try:
            if booking:
                booking.weekday = update_booking.get("weekday", booking.weekday),
                booking.desk_id = update_booking.get("desk_id", booking.desk_id),
                booking.week_id = update_booking.get("week_id", booking.week_id)

                stmt = db.select(Booking).filter_by(booking_ref=booking.get_booking_ref(booking.desk_id, booking.week_id, booking.weekday))
                conflicting_booking = db.session.scalar(stmt)

                if not conflicting_booking or conflicting_booking.id == id:
                    db.session.commit()
                    return BookingSchema().dump(booking), 200
                else:
                    return {"message" : "Desk is unavailable - please try a different desk/time"}, 409
        except (TypeError, AttributeError, IntegrityError, DataError):
            return {"message" : "User and/or booking not found"}, 404


# The DELETE route endpoint (delete existing)
# @jwt_required()
@booking.route("/<int:id>", methods=["DELETE"])
def delete_booking(employee_id, id):
    stmt = db.select(User).filter_by(employee_id=employee_id)
    user = db.session.scalar(stmt)

    try:
        if user:
            authorise(user.id)

            stmt = db.select(Booking).filter_by(user_id=employee_id, id=id)
            booking = db.session.scalar(stmt)

            if booking:
                db.session.delete(booking)
                db.session.commit()
                return {}, 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "User and /or booking not found"}, 404






# The DELETE route endpoint (delete ALL)
@jwt_required()
@booking.route("/", methods=["DELETE"])
def delete_bookings(employee_id):
    stmt = db.select(User).filter_by(employee_id=employee_id)
    user = db.session.scalar(stmt)

    try:
        if user:
            authorise(user.id)

            stmt = None
            stmt = db.select(Booking)
            bookings = db.session.scalars(stmt)


            for booking in bookings:
                if booking.user_id == employee_id:
                    db.session.delete(booking)

            db.session.commit()
            return {}, 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "No bookings found"}, 404

