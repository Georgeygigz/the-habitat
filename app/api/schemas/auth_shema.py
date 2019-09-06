from marshmallow import fields, Schema
from app.api.utils.validation_error import ValidationError

from app.api.models.auth_modles import User
from .base_schema import BaseSchema


class UserSchema(BaseSchema):
    user_id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()
    user_type = fields.Str()
