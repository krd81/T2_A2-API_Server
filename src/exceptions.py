from flask_jwt_extended.exceptions import InvalidHeaderError


def InvalidHeaderError ():
    return {"message" : "You must be logged in to access this resource"}, 401