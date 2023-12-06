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

    json_data = [
            
        {"id": "2024_1",
        "mon": "2024-01-01",
        "tue": "2024-01-02",
        "wed": "2024-01-03",
        "thu": "2024-01-04",
        "fri": "2024-01-05"
        },
        {
        "id": "2024_2",
        "mon": "2024-01-08",
        "tue": "2024-01-09",
        "wed": "2024-01-10",
        "thu": "2024-01-11",
        "fri": "2024-01-12"
        },
        {
        "id": "2024_3",
        "mon": "2024-01-15",
        "tue": "2024-01-16",
        "wed": "2024-01-17",
        "thu": "2024-01-18",
        "fri": "2024-01-19"
        }]
            

    dates = []

    with open ('./client_specs/dates_2024.json') as d:
        dates = json.load(d)

    
    db.session.add_all(dates)
    db.session.commit()

    depts = []
    for dept in DEPARTMENTS:        
        depts.append(dept)

    db.session.add_all(depts)
    db.session.commit()


    desks = []
    for desk in DESKS_1:
        depts.append(desk)

    for desk in DESKS_2:
        depts.append(desk)

    for desk in DESKS_3:
        depts.append(desk)

    db.session.add_all(desks)
    db.session.commit()




    users = [
        User(
            employee_id = "312093",
            f_name = "Kathy",
            l_name = "Morrison",
            email = "kathy.morrison@company.com",
            password = "candle12",
            is_admin = "True",
            dept_id = depts[6].id
        ),
        User(
            employee_id = "215290",
            f_name = "Richard",
            l_name = "Lawson",
            email = "richard.lawson@company.com",
            password = "dancing22",

            dept_id = depts[0].id
        ),
        User(
            employee_id = "485981",
            f_name = "Hannah",
            l_name = "Fisher",
            email = "hannah.fisher@company.com",
            password = "unicorn55",

            dept_id = depts[2].id
        ),
        User(
            employee_id = "525955",
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
            weekday = "",
            desk_id = "",
            user_id = "",
            week_id = ""
        ),
        Booking(
            weekday = "",
            desk_id = "",
            user_id = "",
            week_id = ""
        ),
        Booking(
            weekday = "",
            desk_id = "",
            user_id = "",
            week_id = ""
        ),
        Booking(
            weekday = "",
            desk_id = "",
            user_id = "",
            week_id = ""
        ),
        Booking(
            weekday = "",
            desk_id = "",
            user_id = "",
            week_id = ""
        ),
    ]


    db.session.add_all(bookings)
    db.session.commit()

    db.session.add_all()
    db.session.commit()


    # db.session.add_all()
    # db.session.commit()

    # db.session.add_all()
    # db.session.commit()


    print("Database seeded")