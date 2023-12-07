from app import db
from flask import Blueprint
from app import bcrypt
from models.booking import *
from models.booking_date import *
from models.dept import *
from models.desk import *
from models.user import *
from client_specs.company_x import *
import json

db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def db_create():
    db.drop_all()
    db.create_all()
    print("Created tables")


@db_commands.cli.command("seed")
def db_seed():

    dates_json = []
    dates = []

    with open ('./client_specs/dates_2024.json') as f:
        dates_json = json.load(f)

    for date in dates_json:
        d = Date(
            id = date.get("id"),
            mon = date.get("mon"),
            tue = date.get("tue"),
            wed = date.get("wed"),
            thu = date.get("thu"),
            fri = date.get("fri")
        )
        dates.append(d)
    
    db.session.add_all(dates)
    db.session.commit()

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
            id = "312093",
            f_name = "Kathy",
            l_name = "Morrison",
            email = "kathy.morrison@company.com",
            password = "candle12",
            is_admin = True,
            dept_id = depts[6].id
        ),
        User(
            id = "215290",
            f_name = "Richard",
            l_name = "Lawson",
            email = "richard.lawson@company.com",
            password = "dancing22",

            dept_id = depts[0].id
        ),
        User(
            id = "485981",
            f_name = "Hannah",
            l_name = "Fisher",
            email = "hannah.fisher@company.com",
            password = "unicorn55",

            dept_id = depts[2].id
        ),
        User(
            id = "525955",
            f_name = "Craig",
            l_name = "Stevenson",
            email = "craig.stevenson@company.com",
            password = "cricket07",

            dept_id = depts[1].id
        ),
    ]

    db.session.add_all(users)
    db.session.commit()

    bookings = [
        Booking(
            weekday = "wed",
            desk_id = "3A_02",
            user_id = users[0].id,
            week_id = "2024_1"
        ),
        Booking(
            weekday = "wed",
            desk_id = "2B_05",
            user_id = users[1].id,
            week_id = "2024_1"
        ),
        Booking(
            weekday = "fri",
            desk_id = "3A_02",
            user_id = users[0].id,
            week_id = "2024_2"
        ),
        Booking(
            weekday = "mon",
            desk_id = "1B_01",
            user_id = users[2].id,
            week_id = "2024_2"
        ),
        Booking(
            weekday = "tue",
            desk_id = "1B_01",
            user_id = users[2].id,
            week_id = "2024_1"
        ),
    ]


    db.session.add_all(bookings)
    db.session.commit()

    print("Database seeded")

