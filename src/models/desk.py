from app import db, ma
from marshmallow import fields

# Alchemy is 
class Desk(db.Model):
    # Custom table name to be used in Postgres DB
    __tablename__ = "desks"
    
    # Establishes the entity attributes as columns in the table, together with their data types
    # Primary key tells Alchemy that this is the entity it will treat as the unique identifier for each object
    # Auto-increment=False has been set as desks have a custom id - so this tells Alchemy that the DB administrators
    # will take care of this ID
    id = db.Column(db.String(23), primary_key=True, autoincrement=False)
    available = db.Column(db.Boolean, default=True)

    # Establishes a one to many relationship between desk and booking
    # Back-populates tells SQLAlchemy that Desk's 'booking' attribute is related to Booking's 'desk' attribute
    bookings = db.relationship('Booking', back_populates = "desk")





class DeskSchema(ma.Schema):
    bookings = fields.Nested("BookingSchema", many=True, exclude=["desk_id", "user"])
    # bookings = fields.Nested("BookingSchema", many=True)


    class Meta:
        fields = ("id", "available", "bookings")
