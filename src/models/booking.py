from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, And, Length
from models.booking_date import *
from datetime import datetime

DAYS = ("mon", "tue", "wed", "thu", "fri")

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.String(3), nullable=False)
    date_created = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))

    desk_id = db.Column(db.String, db.ForeignKey("desks.id"), nullable=False)
    desk = db.relationship("Desk", back_populates = "bookings")

    user_id = db.Column(db.String, db.ForeignKey("users.employee_id"), nullable=False)
    user = db.relationship("User", back_populates = "bookings")

    week_id = db.Column(db.String, db.ForeignKey("dates.id"))
    week = db.relationship("Date") # No need to populate the booking_date table

    day = "wed"

    # booking_date = getattr(db.select(Date).filter_by(id=week_id), "wed")
    # booking_date = db.select([Date.dates.c.wed]).where(Date.dates.week_id == week_id)
    stmt = db.select(Date).filter_by(id=week_id)
    # get_dates = db.session.scalar(stmt)
    dates = DateSchema().dump(stmt)
    booking_date = dates.get(str(weekday))
    # Accessing the date in the week will be carried out by the controller

class BookingSchema(ma.Schema):
    weekday = fields.String(validate=OneOf(DAYS))
    desk = fields.Nested("DeskSchema", only=["id"])
    user = fields.Nested("UserSchema", exclude=["password", "is_admin", "bookings"])
    booking_date = fields.Date("dd/mm/yyyy")

    class Meta:
        fields = ("id", "user", "desk", "week.id", "weekday", "booking_date", "date_created")