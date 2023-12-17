from app import db, ma
from marshmallow import fields



class Dept(db.Model):
    # Custom table name is set
    __tablename__ = "departments"

    # Establishes the entity attributes as columns in the table, together with their data types
    # Primary key tells Alchemy that this is the entity it will treat as the unique identifier for each object
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Establishes a one to many relationship between department and user
    # Back-populates tells SQLAlchemy that Dept's 'users' attribute is related to User's 'dept' attribute
    users = db.relationship("User", back_populates = "dept")



class DeptSchema(ma.Schema):
    name = fields.String(required=True)
    users = fields.Nested("UserSchema", many=True, only=["employee_id", "f_name", "l_name"])

    class Meta:
        fields = ("id", "name", "users")

