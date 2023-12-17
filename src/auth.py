from flask import abort,make_response,jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db, jwt
from models.user import User

# Important method used in every route to handle the authentication and authorisation
# of users - it accepts 2 objects in order to cover admin only routes and user-specific routes
@jwt_required()
def authorise(user_id=None, admin_only=False):
    jwt_user_id = get_jwt_identity()
    # Call to database to find user whose id matches the id within the JWT
    stmt = db.select(User).filter_by(id=jwt_user_id)
    # User object converted into individual elements with scalar
    user = db.session.scalar(stmt)

    # If statement concisely handles the scenarios of admin only routes and where the route is allowed
    # for the user to access their own information
    if admin_only == True:
        if not user.is_admin:
            abort(make_response(jsonify(message = "You are not authorised to access this resource")), 401)
    elif not (user.is_admin or (jwt_user_id == user_id)):
            abort(make_response(jsonify(message = "You are not authorised to access this resource")), 401)


# Error handler for missing/expired tokens
# Token exists but is incorrect/expired
@jwt.invalid_token_loader
# Token not present
@jwt.unauthorized_loader
def unauthorised_user(error):
    error
    return {"error": "You are not authorised to access this resource"}, 401


