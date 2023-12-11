from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, And, Length
from models.booking_date import *

from datetime import datetime, timedelta

DAYS = ("mon", "tue", "wed", "thu", "fri")

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    # booking_date_id = db.relationship("Date", back_populates = "id")

    weekday = db.Column(db.String(3), nullable=False)
    booking_date_weekday = db.relationship("Date", back_populates = "weekday")
    date_created = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))

    desk_id = db.Column(db.String, db.ForeignKey("desks.id"), nullable=False)
    desk = db.relationship("Desk", back_populates = "bookings")

    user_id = db.Column(db.String, db.ForeignKey("users.employee_id"), nullable=False)
    user = db.relationship("User", back_populates = "bookings")

    week_id = db.Column(db.Integer, nullable=False)
    booking_date_week = db.relationship("Date", back_populates = "week") 
    
    # booking_date_id = db.Column(db.String, db.ForeignKey("booking_dates.booking_day_id"), unique=False)
    booking_date = db.relationship("Date", back_populates = "booking_day_id")



class BookingSchema(ma.Schema):
    weekday = fields.String(validate=OneOf(DAYS))
    desk = fields.Nested("DeskSchema", only=["id"])
    user = fields.Nested("UserSchema", exclude=["id", "password", "is_admin", "bookings"])
    booking_date = fields.Nested("Date")



    class Meta:
        fields = ("id", "user", "user.employee_id", "desk_id", "week_id", "weekday", "date_created", "booking_date", "booking_day_id")
'''
class Misc():
        def calc_booking_date(week_id, weekday):
            start_date = datetime(2024, 1, 1)
            booking_date = datetime(2024, 1, 1)
            add_weeks = (Booking.week_id - 1) * 7
            add_days = 0
            if (weekday == "tue"):
                add_days = 1
            elif (weekday == "wed"):
                add_days = 2
            elif (weekday == "thu"):
                add_days = 3
            elif (weekday == "fri"):
                add_days = 4

            booking_date = start_date + add_weeks + add_days
            return booking_date
'''
