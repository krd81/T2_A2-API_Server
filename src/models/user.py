from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, And, Length

class User(db.Model):
    __tablename__ = "users"

    employee_id = db.Column(db.String(10), primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    dept_id =  db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    dept = db.relationship("Dept", back_populates = "users")

    bookings = db.relationship("Booking", back_populates = "user")




class ClassSchema(ma.Schema):
    dept = fields.Nested("DeptSchema", only=["name"])
    bookings = fields.Nested("BookingSchema", only=["id", "desk_id"])

    class Meta:
        fields = ("employee_id", "f_name", "l_name", "email", "password", "is_admin", "dept.name", "bookings")
