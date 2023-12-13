from app import db, ma
from marshmallow import fields
# from marshmallow.validate import OneOf, Regexp, And, Length
# from client_specs.company_x import DEPARTMENTS

class Dept(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # users = db.relationship("User", back_populates = "dept", cascade= "all, delete")
    users = db.relationship("User", back_populates = "dept")



class DeptSchema(ma.Schema):
    name = fields.String(required=True)
    users = fields.Nested("UserSchema", many=True, only=["employee_id", "f_name", "l_name"])

    class Meta:
        fields = ("id", "name", "users")

# # Required to allow the creation of a new department 
# class NewDeptSchema(ma.Schema):
#     name = fields.String(required=True)
#     class Meta:
#         fields = ("id", "name")
