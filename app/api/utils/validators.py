import re
from app.api.models.auth_modles import User
from flask import request
from functools import wraps

def check_valid_email(func):
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        try:
            if not re.match(
                r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$',
                    request.json['email']):
                return {"message": "invalid Email"}, 400
            return func(*args, **kwargs)
        except Exception as e:
            return {"message": e}
    return wrapper_function


def check_valid_password(func):
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        try:
            if not re.match(
            '(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@#$])',
                request.json['password']):
                return {"message": "invalid password"}, 400
            return func(*args, **kwargs)
        except Exception as e:
            return {"message": e}
    return wrapper_function


def check_user_if_exist(func):
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        users = User.query.all()
        data = request.get_json(force=True)
        email = data['email']
        try:
            current_user = [user for user in users if user.email == email]
            if current_user:
                return {"message": "{} Already Exist".format(current_user[0].email)}, 409
            return func(*args, **kwargs)
        except Exception as e:
            return {"message": e}
    return wrapper_function
