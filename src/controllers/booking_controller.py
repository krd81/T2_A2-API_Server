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

# Some routes (ie: create new, edit, delete need to be accessed via the user controller)


booking = Blueprint('booking', __name__, url_prefix='/<string:employee_id>/booking')
unauthorised_user

# The GET route endpoint (show all for individual user)
@booking.route('/')
def get_bookings(employee_id):
    stmt = db.select(Booking).filter_by(employee_id=employee_id)
    bookings = db.session.scalars(stmt)

    return BookingSchema(many=True), 200


# The GET route endpoint (show booking)
@booking.route('/<int:id>') # /booking/booking_id [GET]
def get_booking(employee_id, id):
    stmt = db.select(Booking).filter_by(employee_id=employee_id, id=id)
    booking = db.session.scalar(stmt)

    if booking:
        return BookingSchema().dump(booking)
    else:
        return {'message' : 'booking not found - please try again'}, 404



# The POST route endpoint (create new)
@booking.route('/', methods=['POST']) # /user_id/booking [POST]
def new_booking(employee_id):
    new_booking = BookingSchema().load(request.json)

    booking = Booking (
        weekday = new_booking["weekday"],
        desk_id = new_booking["desk_id"],
        employee_id = employee_id,
        week_id = new_booking["week_id"]
    )

    db.session.add(booking)
    db.session.commit()

    return BookingSchema().dump(booking), 201



# The PUT route endpoint (edit existing) # /user_id/booking/booking_id [PUT]
@booking.route('/<int:id>', methods=['PUT', 'PATCH'])
def edit_booking(employee_id, id):
    update_booking = BookingSchema().load(request.json)
    stmt = db.select(Booking).filter_by(employee_id=employee_id, id=id)
    booking = db.session.scalar(stmt)

    if booking:
        booking.weekday = update_booking.get("weekday", booking.weekday),
        booking.desk_id = update_booking.get("desk_id", booking.desk_id),
        booking.employee_id = employee_id,
        booking.week_id = update_booking.get("week_id", booking.week_id)

        db.session.commit()
    else:
        return {'message' : 'booking not found - please try again'}, 404        

    


# The DELETE route endpoint (delete existing) # /user_id/booking/booking_id [DELETE]
@booking.route('/<int:id>', methods=['DELETE'])
def delete_booking(employee_id, id):
    stmt = db.select(Booking).filter_by(employee_id=employee_id, id=id)
    booking = db.session.scalar(stmt)

    if booking:
        db.session.delete(booking)
        db.session.commit()
    else:
        return {'message' : 'booking not found - please try again'}, 404        

