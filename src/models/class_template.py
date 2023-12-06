from app import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Regexp, And, Length

class ClassName(db.Model):
    __tablename__ = ""

    id = db.Column(db.Integer, primary_key=True)



class ClassSchema(ma.Schema):
    class Meta:
        fields = ()
