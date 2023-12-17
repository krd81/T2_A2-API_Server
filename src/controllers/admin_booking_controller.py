from flask import Blueprint, request
from app import db
from auth import authorise
from models.booking import *
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError
from marshmallow.exceptions import ValidationError


# ADMIN ONLY FUNCTIONS
# booking_controller and admin_booking_controller both manage bookings, but the admin
# only functions are contained in admin_booking_controller

# ADMIN functions are view all bookings, edit or delete bookings
# If ADMIN needs to view specific user bookings, these must be accessed via the booking_controller routes

# Note, the admin_boooking_controller routes are accessed via the /booking URL and do not include the 
# employee id


# admin_booking route url is defined as an instance of Blueprint which is registered in __init__.py
admin_booking = Blueprint("admin_booking", __name__, url_prefix="/booking")


# The GET route endpoint (show all bookings)
@jwt_required()
@admin_booking.route("/")
def get_bookings():
    try:
        authorise(None, True)
        # Retrieves all bookings using the select function to select Booking class
        stmt = db.select(Booking)
        bookings = db.session.scalars(stmt)

        # The BookingSchema and dump() method serialises the data and returns 
        # the formatted result, excluding nested "user" fields
        return BookingSchema(many=True, exclude=["user"]).dump(bookings), 200
    except TypeError:
        return {"message" : "Not authorised - admin only"}


# The GET route endpoint (show booking)
@jwt_required()
@admin_booking.route("/<int:id>") 
def get_booking(id):
    authorise(None, True)
    # Retrieves booking id specified in URL using the select function to select Booking class
    stmt = db.select(Booking).filter_by(id=id)
    # Converts booking object to its individual elements using 'scalar'
    booking = db.session.scalar(stmt)

    try:
        if booking: # Only executes if a booking was found in the filter
            # The BookingSchema and dump() method serialises the data and returns 
            # the formatted result, excluding nested "user" fields
            return BookingSchema(exclude=["user"]).dump(booking), 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "booking not found"}, 404



# The POST route endpoint (create new) - not required for ADMIN 
# since users should create their own bookings



# The PUT route endpoint (edit existing)
@jwt_required()
@admin_booking.route("/<int:id>", methods=["PUT", "PATCH"])
def edit_booking(id):
    authorise(None, True)
    try:
        # Receives JSON data via the HTTP request which is deserialised using the load() method
        update_booking = BookingSchema().load(request.json)
    except ValidationError:
        return {"message" : "Check booking details entered"}

    #  In order to check the availability status of the selected desk
    # a database call is made to obtain the Desk object that matches the 
    # one identified in the new booking just created
    stmt = db.select(Desk).filter_by(id=update_booking.get("desk_id"))
    
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    desk = db.session.scalar(stmt)

    # Uses the select function to obtain the booking id matching the booking id 
    # parsed in the URL
    stmt = db.select(Booking).filter_by(id=id)
    
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    booking = db.session.scalar(stmt)

    # This if statement is required to cover the event where desk is not among the fields 
    # being amended. In such cases, desk should be set to be whatever it was in the 
    # original booking
    if not desk:
        # Retrieves the desk with the id matching that of the booking object
        stmt = db.select(Desk).filter_by(id=booking.desk_id)
        # and stores it in an object named 'desk' (as individual elements)
        desk = db.session.scalar(stmt)

    try:
        if booking: # Only executes if a booking was found in the filter
            booking.weekday = update_booking.get("weekday", booking.weekday)
            booking.desk_id = update_booking.get("desk_id", booking.desk_id)
            booking.user_id = update_booking.get("user_id", booking.user_id)
            booking.week_id = update_booking.get("week_id", booking.week_id)


            # This database call attempts to find a booking by filtering on the 'booking_ref' attribute
            # using the get_booking_ref() function which concatenates the desk/booking week/booking day
            # to ensure no duplication across these 3 booking details
            db_lookup = db.select(Booking).filter_by(booking_ref=booking.get_booking_ref(booking.desk_id, booking.week_id, booking.weekday))
            #  If a match is found it is stored in the 'conflicting_booking' object using 'scalar'
            # to return the booking as single elements of a booking object
            conflicting_booking = db.session.scalar(db_lookup)

            # if statement is true only if the 'get_desk_status()' method is True (meaning the desk has 
            # an availability status of True) and if there is no conflicting booking, OR if there is a conflicting
            # booking, its booking id matches that of the booking we are editing - since we have already amended the booking
            # to the new details, Python is accessing accessing the object in memory even though it has not yet been committed
            # to the database
            if booking.get_desk_status(desk) and (not conflicting_booking or conflicting_booking.id == id):
                db.session.commit()
                # The BookingSchema and dump() method serialises the data and returns 
                # the formatted result, excluding nested "user" fields
                return BookingSchema(exclude=["user"]).dump(booking), 200
            else:
                return {"message" : "Desk is unavailable - please try a different desk/time"}, 409
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "Booking not found"}, 404



# The DELETE route endpoint (delete existing)
@jwt_required()
@admin_booking.route("/<int:id>", methods=["DELETE"])
def delete_booking(id):
    authorise(None, True)
    # Retrieves booking id specified in URL using the select function to select Booking class
    stmt = db.select(Booking).filter_by(id=id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    booking = db.session.scalar(stmt)

    try:
        if booking: # Only executes if a booking was found in the filter
            # Uses the current session to remove the booking from the database
            db.session.delete(booking)
            # Closes the session and commits the current transaction
            db.session.commit()
            return {}, 200
    except (TypeError, AttributeError, IntegrityError, DataError):
       return {"message" : "booking not found"}, 404



# The DELETE route endpoint (delete all bookings)
@jwt_required()
@admin_booking.route("/", methods=["DELETE"])
def delete_bookings():
    authorise(None, True)
    # Retrieves all bookings using the select function to select Booking class
    stmt = db.select(Booking)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    bookings = db.session.scalars(stmt)
    try:
        if booking: # Only executes if a booking was found in the filter
            for booking in bookings:
                # All bookings are deleted from the database
                db.session.delete(booking)
            # Closes the session and commits the current transaction
            db.session.commit()
            return {}, 200
    except (TypeError, AttributeError, IntegrityError, DataError):
       return {"message" : "no bookings found"}, 404

