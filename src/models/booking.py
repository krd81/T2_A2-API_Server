from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, And, Length
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
    week = db.relationship("Dates") # No need to populate the booking_date table

    

class ClassSchema(ma.Schema):
    weekday = fields.String(validate=OneOf(DAYS))
    desk = fields.Nested("DeskSchema", only=["id"])
    user = fields.Nested("UserSchema", exclude=["password", "is_admin"])

    class Meta:
        fields = ("id", "users.employee_id", "desks.id", "dates.id", "weekday", "date_created")