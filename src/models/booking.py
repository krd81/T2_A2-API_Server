from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, And, Length
from models.booking_date import *

from datetime import datetime, timedelta

DAYS = ("mon", "tue", "wed", "thu", "fri")

class Booking(db.Model):
    __tablename__ = "bookings"

    # def get_week_no(week_id:str):
    #     index = week_id.index("_")+1
    #     week_no = week_id[index:-1]
    #     return week_no
        
    def calc_add_day(week_id, weekday):
        

        add_weeks = (week_id - 1) * 7
        add_days = 0
        if (weekday == "tue"):
            add_days = 1
        elif (weekday == "wed"):
            add_days = 2
        elif (weekday == "thu"):
            add_days = 3
        elif (weekday == "fri"):
            add_days = 4

        add_days = add_weeks + add_days
        return add_days

    



    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.String(3), nullable=False)
    date_created = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))

    desk_id = db.Column(db.String, db.ForeignKey("desks.id"), nullable=False)
    desk = db.relationship("Desk", back_populates = "bookings")

    user_id = db.Column(db.String, db.ForeignKey("users.employee_id"), nullable=False)
    user = db.relationship("User", back_populates = "bookings")

    week_id = db.Column(db.Integer, nullable=False)
    # week = db.relationship("Date") # No need to populate the booking_date table
    
    start_date = datetime(2024, 1, 1)

    booking_date = start_date + calc_add_day(week_id, weekday)
    booking_date_id = db.Column(db.String, default=booking_date)



class BookingSchema(ma.Schema):
    weekday = fields.String(validate=OneOf(DAYS))
    desk = fields.Nested("DeskSchema", only=["id"])
    user = fields.Nested("UserSchema", exclude=["id", "password", "is_admin", "bookings"])



    class Meta:
        fields = ("id", "user", "user.employee_id", "desk_id", "week_id", "weekday", "date_created", "booking_date")
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
