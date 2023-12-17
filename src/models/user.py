from app import db, ma
from marshmallow import fields
from marshmallow.validate import And, Length

class User(db.Model):
    # Custom table name to be used in Postgres DB
    __tablename__ = "users"
    # Establishes the entity attributes as columns in the table, together with their data types
    # Primary key tells Alchemy that this is the entity it will treat as the unique identifier for each object
    id = db.Column(db.Integer, primary_key=True)
    # Unique = True is added since employee_id for the purpose of database calls is effectively the primary key
    # therefore we cannot allow duplicates
    employee_id = db.Column(db.String(10), nullable=False, unique=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # dept_id foreign key provides access to departments from the user table
    # If a department name is updated, it should cascade to the user
    # If a department is deleted, the user's department should be set to null
    dept_id =  db.Column(db.Integer, db.ForeignKey("departments.id", onupdate="cascade", ondelete="set null"), nullable=True)
    # Establishes a one to one relationship between user and department
    # Back-populates tells SQLAlchemy that Desk's 'booking' attribute is related to Booking's 'desk' attribute
    dept = db.relationship("Dept", back_populates = "users")

    # Establishes a one to many relationship between user and bookings    
    # Back-populates tells SQLAlchemy that User's 'bookings' attribute is related to Booking's 'user' attribute
    # Cascade is required so that deleting a user, deletes any associated bookings
    bookings = db.relationship("Booking", back_populates = "user", cascade= "all, delete") 





class UserSchema(ma.Schema):
    dept = fields.Nested("DeptSchema", only=["id", "name"])
    bookings = fields.Nested("BookingSchema", many=True, only=["id", "desk_id", "week_id", "weekday"])
    email = fields.Email()
    password = fields.String(validate=And(Length(min=8, error='Password must be between 8 and 14 characters'), 
                Length(max=14, error='Password must be between 8 and 14 characters')))


    class Meta:
        fields = ("id", "employee_id", "f_name", "l_name", "email", "password", "is_admin", "dept", "dept_id","bookings")


class CreateUserSchema(ma.Schema):
    dept = fields.Nested("DeptSchema")
    dept_id = fields.Integer(required=True)
    bookings = fields.Nested("BookingSchema", only=["id"])
    f_name = fields.String(required=True)
    l_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, 
                validate=And(Length(min=8, error='Password must be between 8 and 14 characters'), 
                Length(max=14, error='Password must be between 8 and 14 characters')))

    class Meta:
        fields = ("id", "employee_id", "f_name", "l_name", "email", "password", "is_admin", "dept_id", "bookings")


class UserSchemaPassword(ma.Schema):
    password = fields.String(required=True, 
                validate=And(Length(min=8, error='Password must be between 8 and 14 characters'), 
                Length(max=14, error='Password must be between 8 and 14 characters')))


    class Meta:
        fields = ("id", "employee_id", "f_name", "l_name", "email", "password", "is_admin", "dept_id", "bookings")


