from marshmallow import fields, post_load, pre_load, Schema
from api.utils.validation_error import ValidationError

from api.models.auth_modles import User

class UserSchema(Schema):
    user_id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()
    user_type = fields.Str()

    def load_object_into_schema(self, data, partial=False):
        """Helper function to load python objects into schema"""
        # import pdb; pdb.set_trace()

        data = self.load(data, partial=partial)
        if data:
            return data
        raise ValidationError(dict(errors=errors, message='An error occurred'), 400)
