from flask import abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from models.user import User

@jwt_required()
def authorise(user_id=None):
    jwt_user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=jwt_user_id)
    user = db.session.scalar(stmt)

    if not (user.is_admin or (user_id and jwt_user_id == user_id)):
        # return {"message" : "You are not authorised to access this resource"}, 401
        abort(401, {"message" : "You are not authorised to access this resource"})