from app import db, ma

from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, And, Length
from datetime import datetime

class Date(db.Model):
    __tablename__ = "booking_dates"
    
    id = db.Column(db.String(7), primary_key=True)
    mon = db.Column(db.String(10), nullable=False, unique=True)
    tue = db.Column(db.String(10), nullable=False, unique=True)
    wed = db.Column(db.String(10), nullable=False, unique=True)
    thu = db.Column(db.String(10), nullable=False, unique=True)
    fri = db.Column(db.String(10), nullable=False, unique=True)
    
    '''
    def calc_booking_day(week_id, weekday):     
        start_date = datetime(2024, 1, 1)
        booking_date = datetime(2024, 1, 1)
        add_weeks = (1 - 1) * 7
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

    # _id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False, primary_key=True)
    # id = db.relationship("Booking", back_populates = "booking_date_id")
    id = db.Column(db.Integer, primary_key=True)

    # week_id = db.Column(db.Integer, db.ForeignKey("bookings.week_id"), unique=False)
    # week = db.relationship("Booking", back_populates = "booking_date_week")
    # week_no = db.session.scalar(week)
    # weekday_id = db.Column(db.String, db.ForeignKey("bookings.weekday"), unique=False)
    # weekday = db.relationship("Booking", back_populates = "booking_date_weekday")

    # booking_date = calc_booking_day(week, weekday)

    # booking_day_id = db.Column(db.Date, default=booking_date)
    # booking_day = db.relationship("Booking", back_populates = "booking_date")


class DateSchema(ma.Schema):
    class Meta:
        fields = ("id",)



