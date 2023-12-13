from flask import Blueprint, request
from app import db
from auth import authorise
from models.booking import *
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError


# ADMIN ONLY FUNCTIONS


admin_booking = Blueprint("admin_booking", __name__, url_prefix="/booking")


# The GET route endpoint (show all)
@jwt_required()
@admin_booking.route("/")
def get_bookings():
    try:
        authorise(None, True)
        db_bookings = db.select(Booking)
        bookings = db.session.scalars(db_bookings)

        return BookingSchema(many=True).dump(bookings), 200
    except TypeError:
        return {"message" : "Not authorised - admin only"}


# The GET route endpoint (show booking)
@jwt_required()
@admin_booking.route("/<int:id>") # /booking/booking_id [GET]
def get_booking(id):
    authorise(None, True)
    stmt = db.select(Booking).filter_by(id=id)
    booking = db.session.scalar(stmt)

    try:
        if booking:
            return BookingSchema().dump(booking), 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "booking not found - please try again"}, 404



# The POST route endpoint (create new) - not required for ADMIN



# The PUT route endpoint (edit existing)
@jwt_required()
@admin_booking.route("/<int:id>", methods=["PUT", "PATCH"])
def edit_booking(id):
    authorise(None, True)
    update_booking = BookingSchema().load(request.json)
    stmt = db.select(Booking).filter_by(id=id)
    booking = db.session.scalar(stmt)

    try:
        if booking:
            booking.weekday = update_booking.get("weekday", booking.weekday)
            booking.desk_id = update_booking.get("desk_id", booking.desk_id)
            booking.user_id = update_booking.get("user_id", booking.user_id)
            booking.week_id = update_booking.get("week_id", booking.week_id)


            db_lookup = db.select(Booking).filter_by(booking_ref=booking.get_booking_ref(booking.desk_id, booking.week_id, booking.weekday))
            conflicting_booking = db.session.scalar(db_lookup)

            if not conflicting_booking or conflicting_booking.id == id:
                db.session.commit()
                return BookingSchema().dump(booking), 200
            else:
                return {"message" : "Desk is unavailable - please try again"}, 409
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "Booking not found - please try again"}, 404



# The DELETE route endpoint (delete existing)
@jwt_required()
@admin_booking.route("/<int:id>", methods=["DELETE"])
def delete_booking(id):
    authorise(None, True)
    stmt = db.select(Booking).filter_by(id=id)
    booking = db.session.scalar(stmt)

    try:
        # if booking:
            db.session.delete(booking)
            db.session.commit()
            return {}, 200
    except (TypeError, AttributeError, IntegrityError, DataError):
       return {"message" : "booking not found - please try again"}, 404




