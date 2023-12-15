from app import db
from flask import Blueprint
from app import bcrypt
from models.booking import *
from models.dept import *
from models.desk import *
from models.user import *
from client_specs.company_x import *


db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def db_create():
    db.drop_all()
    db.create_all()
    print("Created tables")


@db_commands.cli.command("seed")
def db_seed():

    depts = []
    for dept in DEPARTMENTS:
        d = Dept(
            name = dept
        )        
        depts.append(d)

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

    print("Database seeded")

