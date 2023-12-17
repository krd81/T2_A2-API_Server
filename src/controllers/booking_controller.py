from flask import Blueprint, request
from app import db
from auth import authorise
from models.booking import *
from models.user import *
from models.desk import Desk
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError, DataError
from marshmallow.exceptions import ValidationError

# booking_controller and admin_booking_controller both manage bookings, but the admin
# only functions are contained in admin_booking_controller

# USER functions are create booking, view, edit or delete own bookings
# Users can view/delete 1 or all of their own bookings

# The user booking route, requires the employee id as part of the route, so
# this controller is registered via the user_controller


# booking route url is defined as an instance of Blueprint which is registered in user_controller.py
booking = Blueprint("booking", __name__, url_prefix="/<string:employee_id>/booking")



# The GET route endpoint (show all for individual user)
@jwt_required()
@booking.route("/")
def get_bookings(employee_id):
    # Uses the select function to obtain the user whose employee id was parsed via the URL
    stmt = db.select(User).filter_by(employee_id=employee_id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    user = db.session.scalar(stmt)

    try:
        if user: # Only executes if a user was found in the filter        
            authorise(user.id)
            # Uses the select function to obtain any bookings which are associated with the user
            stmt = db.select(Booking).filter_by(user_id=employee_id)
            # The session object creates a session related to the Flask app
            # scalars returns single elements of the database row(s)
            bookings = db.session.scalars(stmt)

            # The BookingSchema and dump() method serialises the data and returns the 
            # formatted result, excluding nested "user" fields
            return BookingSchema(many=True, exclude=["user"]).dump(bookings), 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "No bookings found"}, 404


# The GET route endpoint (show booking)
@jwt_required()
@booking.route("/<int:id>")
def get_booking(employee_id, id):
    # Uses the select function to obtain the user whose employee id was parsed via the URL
    stmt = db.select(User).filter_by(employee_id=employee_id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    user = db.session.scalar(stmt)

    try:
        if user: # Only executes if a user was found in the filter
            authorise(user.id)
            # Uses the select function to obtain the bookings which is associated with the user
            # and matches the booking id parsed in the URL
            stmt = db.select(Booking).filter_by(user_id=employee_id, id=id)
            # The session object creates a session related to the Flask app
            # scalars returns single elements of the database row(s)
            booking = db.session.scalar(stmt)

            if booking: # Only executes if a booking was found in the filter
                # The BookingSchema and dump() method serialises the data and returns the 
                # formatted result, excluding nested "user" fields
                return BookingSchema(exclude=["user"]).dump(booking), 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "Booking not found"}, 404


# The POST route endpoint (create new)
# Due to business logic, which does not allow duplicate bookings or booking desks which 
# are available=False, additional verification is required to make new bookings
@jwt_required()
@booking.route("/", methods=["POST"]) 
def new_booking(employee_id):
    # Uses the select function to obtain the user whose employee id was parsed via the URL
    stmt = db.select(User).filter_by(employee_id=employee_id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    user = db.session.scalar(stmt)

    if user:
        authorise(user.id)
        try:
            # Receives JSON data via the HTTP request which is deserialised using the load() method
            new_booking = BookingSchema().load(request.json)
        except ValidationError:
            return {"message" : "Weekday must be one of 'mon', 'tue', 'wed', 'thu', 'fri'"}, 400

        booking = Booking (
            weekday = new_booking["weekday"],
            desk_id = new_booking["desk_id"],
            user_id = employee_id,
            week_id = new_booking["week_id"]
        )
        
        # This database call attempts to find a booking by filtering on the 'booking_ref' attribute
        # using the get_booking_ref() function which concatenates the desk/booking week/booking day
        # to ensure no duplication across these 3 booking details
        stmt = db.select(Booking).filter_by(booking_ref=booking.get_booking_ref(booking.desk_id, booking.week_id, booking.weekday))

        #  If a match is found it is stored in the 'conflicting_booking' object using 'scalar'
        # to return the booking as single elements of a booking object
        conflicting_booking = db.session.scalar(stmt)
        #  In order to check the availability status of the selected desk
        # a database call is made to obtain the Desk object that matches the 
        # one identified in the new booking just created
        stmt = db.select(Desk).filter_by(id=booking.desk_id)
        # The result is stored as 'selected_desk' and 'scalar' conveniently enables
        # storage of the desk elements, individually, so that the desk status can be checked in the next step
        selected_desk = db.session.scalar(stmt)
        try:
            # if statement is true only if there is no conflicting booking and if
            # the 'get_desk_status()' method is True (meaning the desk has an availability status of True)
            if (not conflicting_booking) and booking.get_desk_status(selected_desk):
                # If all conditions have been met the new booking can be added to the database
                db.session.add(booking)
                # Closes the session and commits the current transaction
                db.session.commit()

                # The BookingSchema and dump() method serialises the data and returns 
                # the formatted result, excluding nested "user" fields
                return BookingSchema(exclude=["user"]).dump(booking), 201
            else:
                return {"message" : "Desk is unavailable"}, 400
        except (IntegrityError, DataError):
            return {"message" : "Invalid input"}, 400
    else:
        return {"message" : "You are not authorised to access this resource"}, 401




# The PUT route endpoint (edit existing) # /user_id/booking/booking_id [PUT]
# Due to business logic, which does not allow duplicate bookings or booking desks which 
# are available=False, additional verification is required to update bookings
@jwt_required()
@booking.route("/<int:id>", methods=["PUT", "PATCH"])
def edit_booking(employee_id, id):
    # Uses the select function to obtain the user whose employee id was parsed via the URL
    stmt = db.select(User).filter_by(employee_id=employee_id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    user = db.session.scalar(stmt)

    if user: # Only executes if a user was found in the filter
        authorise(user.id)

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

        # Uses the select function to obtain the bookings which is associated with the user
        # and matches the booking id parsed in the URL
        stmt = db.select(Booking).filter_by(user_id=employee_id, id=id)
        # The session object creates a session related to the Flask app
        # scalars returns single elements of the database row(s)
        booking = db.session.scalar(stmt)

        # This if statement is required to cover the event where the user is amending fields 
        # other than desk. In such cases, desk should be set to be whatever it was in the 
        # original booking
        if not desk:
            # Retrieves the desk with the id matching that of the booking object
            stmt = db.select(Desk).filter_by(id=booking.desk_id)
            # and stores it in an object named 'desk' (as individual elements)
            desk = db.session.scalar(stmt)


        try:
            if booking: # Only executes if a booking was found matching the id obtained from the URL
                booking.weekday = update_booking.get("weekday", booking.weekday),
                booking.desk_id = update_booking.get("desk_id", booking.desk_id),
                booking.week_id = update_booking.get("week_id", booking.week_id)
                
                # This database call attempts to find a booking by filtering on the 'booking_ref' attribute
                # using the get_booking_ref() function which concatenates the desk/booking week/booking day
                # to ensure no duplication across these 3 booking details
                stmt = db.select(Booking).filter_by(booking_ref=booking.get_booking_ref(booking.desk_id, booking.week_id, booking.weekday))
                
                #  If a match is found it is stored in the 'conflicting_booking' object using 'scalar'
                # to return the booking as single elements of a booking object
                conflicting_booking = db.session.scalar(stmt)

                # if statement is true only if the 'get_desk_status()' method is True (meaning the desk has 
                # an availability status of True) and if there is no conflicting booking, OR if there is a conflicting
                # booking, its booking id matches that of the booking we are editing - since we have already amended the booking
                # to the new details, Python is accessing accessing the object in memory even though it has not yet been committed
                # to the database
                if booking.get_desk_status(desk) and (not conflicting_booking or conflicting_booking.id == id):
                    # Closes the session and commits the current transaction
                    # providing all conditions have been met the updated booking can be committed to the database
                    db.session.commit()
                    # The BookingSchema and dump() method serialises the data and returns 
                    # the formatted result, excluding nested "user" fields
                    return BookingSchema(exclude=["user"]).dump(booking), 200
                else:
                    return {"message" : "Desk is unavailable - please try a different desk/time"}, 409
        except (TypeError, AttributeError, IntegrityError, DataError):
            return {"message" : "User and/or booking not found"}, 404


# The DELETE route endpoint (delete one booking)
# @jwt_required()
@booking.route("/<int:id>", methods=["DELETE"])
def delete_booking(employee_id, id):
    # Uses the select function to obtain the bookings which is associated with the user
    # and matches the booking id parsed in the URL
    stmt = db.select(User).filter_by(employee_id=employee_id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    user = db.session.scalar(stmt)

    try:
        if user: # Only executes if a user was found in the filter
            authorise(user.id)            
            # Uses the select function to obtain the bookings which is associated with the user
            # and matches the booking id parsed in the URL
            stmt = db.select(Booking).filter_by(user_id=employee_id, id=id)
            # The session object creates a session related to the Flask app
            # scalars returns single elements of the database row(s)
            booking = db.session.scalar(stmt)

            if booking: # Only executes if a booking was found in the filter
                # Uses the current session to remove the booking from the database
                db.session.delete(booking)
                # Closes the session and commits the current transaction
                db.session.commit()
                return {}, 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "User and/or booking not found"}, 404






# The DELETE route endpoint (delete ALL bookings)
@jwt_required()
@booking.route("/", methods=["DELETE"])
def delete_bookings(employee_id):
    stmt = db.select(User).filter_by(employee_id=employee_id)
    # The session object creates a session related to the Flask app
    # scalars returns single elements of the database row(s)
    user = db.session.scalar(stmt)

    try:
        if user: # Only executes if a user was found in the filter
            authorise(user.id)
            # Sets 'stmt' to None to mitigate against issues if no bookings are found
            stmt = None
            # Uses the select function to obtain ALL bookings
            stmt = db.select(Booking)
            # The session object creates a session related to the Flask app
            # scalars returns single elements of the database row(s)
            bookings = db.session.scalars(stmt)


            for booking in bookings:
                if booking.user_id == employee_id:
                    # Any booking which is associated with the user is deleted
                    db.session.delete(booking)
            # Closes the session and commits the current transaction
            db.session.commit()
            return {}, 200
    except (TypeError, AttributeError, IntegrityError, DataError):
        return {"message" : "No bookings found"}, 404

