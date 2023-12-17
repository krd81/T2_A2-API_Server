from app import db, ma
from sqlalchemy import func
from models.desk import *
from marshmallow import fields
from marshmallow.validate import OneOf
from datetime import datetime

DAYS = ("mon", "tue", "wed", "thu", "fri")

class Booking(db.Model):
    # Custom table name to be used in Postgres DB
    __tablename__ = "bookings"

    # Establishes the entity attributes as columns in the table, together with their data types
    # Primary key tells Alchemy that this is the entity it will treat as the unique identifier for each object
    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.String(3), nullable=False) # Day of the week the booking is for
    date_created = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))
    week_id = db.Column(db.Integer, nullable=False)

    # desk_id foreign key provides access to desks from the bookings table
    # If a desk_id is updated, it should cascade to any bookings
    # Desks cannot be deleted if there are bookings, therefore no constraint for ondelete is given
    desk_id = db.Column(db.String, db.ForeignKey("desks.id", onupdate="cascade"), nullable=False)

    # Establishes a one to one relationship between booking and desk
    # Back-populates tells SQLAlchemy that Booking's 'desk' attribute is related to Desk's 'bookings' attribute
    desk = db.relationship("Desk", back_populates = "bookings")


    # user_id foreign key provides access to users from the bookings table
    # If a user is updated, the changes should cascade to any bookings
    # If a user is deleted, this should cascade to (delete) any associated bookings
    user_id = db.Column(db.String, db.ForeignKey("users.employee_id", onupdate="cascade", ondelete="cascade"), nullable=False)

    # Establishes a one to one relationship between user and department
    # Back-populates tells SQLAlchemy that Booking's 'user' attribute is related to User's 'bookings' attribute
    # Passive-deletes has been used as a failsafe to handle any discrepancy that may occur in SQLAlchemy actioning 
    # the DELETE user command to ensure that the user's bookings are deleted
    user = db.relationship("User", back_populates = "bookings", passive_deletes="all")

    

    # This method is used by booking_controller / admin_booking_controller to ensure 
    # no duplicate bookings of the same desk on the same day by more than one user
    def get_booking_ref(self, desk, week, day):
        booking_ref = func.concat(desk, week, day)
        return booking_ref

    booking_ref = get_booking_ref(None, desk_id, week_id, weekday)

    # This method is used to obtain the desk's availability status
    # If a desk has been set as being 'unavailable' it is not allowed
    # to be booked (called by booking_controller / admin_booking_controller)
    def get_desk_status(self, desk):
        new_desk = Desk(id = desk.id, available = desk.available)
        desk = DeskSchema(only=["available"]).dump(new_desk)
        available = desk.get("available")
        return available




class BookingSchema(ma.Schema):
    weekday = fields.String(validate=OneOf(DAYS, error="Day entered was not recognised"))
    desk = fields.Nested("DeskSchema", exclude=["bookings"])
    user = fields.Nested("UserSchema", exclude=["id", "password", "is_admin", "bookings"])


    class Meta:
        fields = ("id", "user", "user.employee_id", "desk_id", "desk_available", "week_id", "weekday", "date_created")

