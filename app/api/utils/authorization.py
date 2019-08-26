# app/api/v1/utils/authorization

from flask_jwt_extended import get_jwt_identity
from functools import wraps

from app.api.models.auth_modles import User

def admin_required(func):
    """ Admin Rights."""
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        users = User.query.all()
        try:
            cur_user = [
                user for user in users if user.email == get_jwt_identity()]
            user_role = cur_user[0].user_type
            if user_role != 'admin':
                return {
                    'message': 'This activity can be completed by Admin only'}, 403 # Forbidden
            return func(*args, **kwargs)
        except Exception as e:
            return {"message": e}
    return wrapper_function


def store_attendant_required(func):
    """Store attedant rights."""
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        users = User.query.all()
        cur_user = [user for user in users if user.email
                    == get_jwt_identity()]
        user_role = cur_user[0].user_type
        if user_role != 'attedant': 
            return {
                'message': 'This activity can be completed by Store Attedant only'}, 403 # Forbidden
        return func(*args, **kwargs)
    return wrapper_function
