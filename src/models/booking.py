from app import db, ma
from sqlalchemy import func
from marshmallow import fields
from marshmallow.validate import OneOf
from datetime import datetime

DAYS = ("mon", "tue", "wed", "thu", "fri")

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    weekday = db.Column(db.String(3), nullable=False)
    date_created = db.Column(db.Date, default=datetime.now().strftime('%Y-%m-%d'))

    desk_id = db.Column(db.String, db.ForeignKey("desks.id"), onupdate="cascade", nullable=False)
    desk = db.relationship("Desk", back_populates = "bookings")

    # On delete set null or cascade?
    user_id = db.Column(db.String, db.ForeignKey("users.employee_id", onupdate="cascade", ondelete="cascade"), nullable=False)
    user = db.relationship("User", back_populates = "bookings", passive_deletes="all")

    week_id = db.Column(db.Integer, nullable=False)


    def get_booking_ref(self, desk, week, day):
        booking_ref = func.concat(desk, week, day)
        return booking_ref

    booking_ref = get_booking_ref(None, desk_id, week_id, weekday)



class BookingSchema(ma.Schema):
    weekday = fields.String(validate=OneOf(DAYS, error="Day entered was not recognised"))
    desk = fields.Nested("DeskSchema", only=["id"])
    user = fields.Nested("UserSchema", exclude=["id", "password", "is_admin", "bookings"])


    class Meta:
        fields = ("id", "user", "user.employee_id", "desk_id", "week_id", "weekday", "date_created", "booking_date", "booking_day_id")

