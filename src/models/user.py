from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, And, Length

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(10), primary_key=True) # Employee ref no
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    dept_id =  db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    dept = db.relationship("Dept", back_populates = "users")

    bookings = db.relationship("Booking", back_populates = "user")




class UserSchema(ma.Schema):
    dept = fields.Nested("DeptSchema", only=["name"])
    bookings = fields.Nested("BookingSchema", only=["id"])
    f_name = fields.String(required=True)
    l_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, 
                validate=And(Length(min=8, error='Password must be between 8 and 14 characters'), 
                Length(max=14, error='Password must be between 8 and 14 characters')))

    class Meta:
        fields = ("id", "f_name", "l_name", "email", "password", "is_admin", "dept_id", "bookings")
