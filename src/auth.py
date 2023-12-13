from flask import abort,make_response,jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db, jwt
from models.user import User

# Add extra parameter to give functionality for ADMIN ONLY

@jwt_required()
def authorise(user_id=None, admin_only=False):
    jwt_user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)

    if admin_only == True:
        if not user.is_admin:
            abort(make_response(jsonify(message = "You are not authorised to access this resource")), 401)
    # elif not (user.is_admin or (user_id and jwt_user_id == user_id)):
    elif not (user.is_admin or (jwt_user_id == user_id)):
            abort(make_response(jsonify(message = "You are not authorised to access this resource")), 401)


# Token exists but is incorrect/expired
@jwt.invalid_token_loader
# Token not present
@jwt.unauthorized_loader
def unauthorised_user(error):
    error
    return {"error": "You are not authorised to access this resource"}, 401