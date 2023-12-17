from app import db
from flask import Blueprint
from app import bcrypt
from models.booking import *
from models.dept import *
from models.desk import *
from models.user import *


# the db_commands instance of Blueprint which is registered in __init__.py
db_commands = Blueprint("db", __name__)


DEPARTMENTS = ["Finance", "IT", "Legal", "Marketing", "Customer Service", "Sales", "HR", "Executive"]

# Desks
# Level 1
DESKS_1 = ["1A_01", "1A_02", "1A_03", "1A_04", "1A_05", "1B_01", "1B_02", "1B_03", "1B_04", "1B_05"]

# Level 2
DESKS_2 = ["2A_01", "2A_02", "2A_03", "2A_04", "2A_05", "2B_01", "2B_02", "2B_03", "2B_04", "2B_05"]

# Level 3
DESKS_3 = ["3A_01", "3A_02", "3A_03", "3A_04", "3A_05", "3B_01", "3B_02", "3B_03", "3B_04", "3B_05"]

ALL_DESKS = DESKS_1 + DESKS_2 + DESKS_3



# db_commands.cli allow terminal commands to be formed within the app
# and executed by the command line interface
@db_commands.cli.command("create")
def db_create():
    # In testing, whenever changes are made the database tables must be dropped and re-created
    db.drop_all()
    db.create_all()
    print("Created tables")

# Once the tables have been re-created, they can be re-seeded with the sample data
@db_commands.cli.command("seed")
def db_seed():

    depts = []
    for dept in DEPARTMENTS:
        d = Dept(
            name = dept
        )        
        depts.append(d)

    # Each tables elements are added then committed to avoid any data inconsistency issues
    db.session.add_all(depts)
    db.session.commit()


    desks = []
    for desk in ALL_DESKS:
        d = Desk(
            id = desk
        )
        desks.append(d)

    db.session.add_all(desks)
    db.session.commit()



    users = [
        User(
            employee_id = "312093",
            f_name = "Kathy",
            l_name = "Morrison",
            email = "kathy.morrison@company.com",
            password = bcrypt.generate_password_hash("candle12").decode("utf8"),
            is_admin = True,
            dept_id = depts[6].id
        ),
        User(
            employee_id = "215290",
            f_name = "Richard",
            l_name = "Lawson",
            email = "richard.lawson@company.com",
            password = bcrypt.generate_password_hash("dancing22").decode("utf8"),

            dept_id = depts[0].id
        ),
        User(
            employee_id = "485981",
            f_name = "Hannah",
            l_name = "Fisher",
            email = "hannah.fisher@company.com",
            password = bcrypt.generate_password_hash("unicorn55").decode("utf8"),

            dept_id = depts[2].id
        ),
        User(
            employee_id = "525955",
            f_name = "Craig",
            l_name = "Stevenson",
            email = "craig.stevenson@company.com",
            password = bcrypt.generate_password_hash("cricket07").decode("utf8"),
            dept_id = depts[1].id
        ),
    ]

    db.session.add_all(users)
    db.session.commit()

    bookings = [
        Booking(
            weekday = "wed",
            desk_id = "3A_02",
            user_id = users[0].employee_id,
            week_id = "1"
        ),
        Booking(
            weekday = "wed",
            desk_id = "2B_05",
            user_id = users[1].employee_id,
            week_id = "1"
        ),
        Booking(
            weekday = "fri",
            desk_id = "3A_02",
            user_id = users[0].employee_id,
            week_id = "2"
        ),
        Booking(
            weekday = "mon",
            desk_id = "1B_01",
            user_id = users[2].employee_id,
            week_id = "2"
        ),
        Booking(
            weekday = "tue",
            desk_id = "1B_01",
            user_id = users[2].employee_id,
            week_id = "1"
        ),
    ]


    
    db.session.add_all(bookings)
    db.session.commit()
    # Once all data is added and committed, the database is ready for use

    print("Database seeded")

