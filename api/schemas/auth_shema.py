from marshmallow import fields, post_load, pre_load, Schema
from api.utils.validation_error import ValidationError

from api.models.auth_modles import User
from .base_schema import BaseSchema


class UserSchema(BaseSchema):
    user_id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()
    user_type = fields.Str()
