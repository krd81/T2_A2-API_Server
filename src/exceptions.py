from app import db
from flask_jwt_extended.exceptions import InvalidHeaderError


def InvalidHeaderError ():
    return {"message" : "You must be logged in to access this resource"}, 401

@db.errorhandler(404)
def not_found(error):
    return {"error" : "Requested URL does not exist"}