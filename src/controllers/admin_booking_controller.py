from flask import Blueprint, request
from app import db, unauthorised_user, bcrypt
from auth import authorise
from models.booking import *
# from models.booking_date import * #???
from flask_jwt_extended import jwt_required, create_access_token
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta

# ADMIN ONLY FUNCTIONS


admin_booking = Blueprint('admin_booking', __name__, url_prefix='/booking')
# unauthorised_user() 

# The GET route endpoint (show all)
@jwt_required()
@admin_booking.route('/')
def get_bookings():
    try:
        authorise()
        db_bookings = db.select(Booking)
        bookings = db.session.scalars(db_bookings)

        return BookingSchema(many=True).dump(bookings), 200
    except TypeError:
        return {"message" : "Not authorised - admin only"}


# The GET route endpoint (show booking)
@jwt_required()
@admin_booking.route('/<int:id>') # /booking/booking_id [GET]
def get_booking(id):
    authorise()
    stmt = db.select(Booking).filter_by(id=id)
    booking = db.session.scalar(stmt)
    
    if booking:
        return BookingSchema().dump(booking), 200
    else:
        return {'message' : 'booking not found - please try again'}, 404



# The POST route endpoint (create new) - not required for ADMIN



# The PUT route endpoint (edit existing) 
@jwt_required()
@admin_booking.route('/<int:id>', methods=['PUT', 'PATCH'])
def edit_booking(id):
    authorise()
    update_booking = BookingSchema().load(request.json)
    stmt = db.select(Booking).filter_by(id=id)
    booking = db.session.scalar(stmt)

    if booking:
        booking.weekday = update_booking.get("weekday", booking.weekday)
        booking.desk_id = update_booking.get("desk_id", booking.desk_id)
        booking.user_id = update_booking.get("user_id", booking.user_id)
        booking.week_id = update_booking.get("week_id", booking.week_id)

        db.session.commit()
        return BookingSchema().dump(booking), 200
    else:
        return {'message' : 'booking not found - please try again'}, 404



# The DELETE route endpoint (delete existing)
@jwt_required()
@admin_booking.route('/<int:id>', methods=['DELETE'])
def delete_booking(id):
    authorise()
    stmt = db.select(Booking).filter_by(id=id)
    booking = db.session.scalar(stmt)

    if booking:
        db.session.delete(booking)
        db.session.commit()
        return {}, 200
    else:
       return {'message' : 'booking not found - please try again'}, 404 




