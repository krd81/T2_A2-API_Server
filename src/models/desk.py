from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, And, Length

class Desk(db.Model):
    __tablename__ = "desks"

    id = db.Column(db.String(6), primary_key=True, autoincrement=False)
    available = db.Column(db.Boolean, default=True)

    bookings = db.relationship('Booking', back_populates = "desk")




class DeskSchema(ma.Schema):
    bookings = fields.Nested("BookingSchema")

    class Meta:
        fields = ("id", "available", "bookings")
