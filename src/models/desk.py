from app import db, ma
from marshmallow import fields

# Alchemy is 
class Desk(db.Model):
    __tablename__ = "desks"

    id = db.Column(db.String(23), primary_key=True, autoincrement=False)
    available = db.Column(db.Boolean, default=True)

    bookings = db.relationship('Booking', back_populates = "desk")





class DeskSchema(ma.Schema):
    bookings = fields.Nested("BookingSchema", many=True, exclude=["desk_id", "user"])
    # bookings = fields.Nested("BookingSchema", many=True)


    class Meta:
        fields = ("id", "available", "bookings")
