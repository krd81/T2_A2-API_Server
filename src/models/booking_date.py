from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, And, Length
from datetime import date

class Date(db.Model):
    __tablename__ = "dates"

    id = db.Column(db.String(7), primary_key=True, autoincrement=False)
    mon = db.Column(db.String(10), nullable=False, unique=True)
    tue = db.Column(db.String(10), nullable=False, unique=True)
    wed = db.Column(db.String(10), nullable=False, unique=True)
    thu = db.Column(db.String(10), nullable=False, unique=True)
    fri = db.Column(db.String(10), nullable=False, unique=True)



class DateSchema(ma.Schema):
    class Meta:
        fields = ("id", "mon", "tue", "wed", "thu", "fri")
