from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, And, Length

class Desk(db.Model):
    __tablename__ = "desks"

    id = db.Column(db.String(23), primary_key=True, autoincrement=False)
    available = db.Column(db.Boolean, default=True)

    # bookings = db.relationship('Booking', back_populates = "desk", cascade= "all, delete")
    bookings = db.relationship('Booking', back_populates = "desk")




class DeskSchema(ma.Schema):
    bookings = fields.Nested("BookingSchema", many=True, exclude=["desk_id"])

    class Meta:
        fields = ("id", "available", "bookings")
