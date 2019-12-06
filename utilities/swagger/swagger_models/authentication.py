"""
Model Definition for request collection
"""

from flask_restplus import fields
from ..collections.authentication import register_namespace

# swagger model that defines request fields
register_model = register_namespace.model(
    "request_model", {
        'username': fields.String(
            required=True, description='username'
        ),
        'email': fields.String(
            required=True, description='user email'
        ),
        'password': fields.String(
            required=True, description='user password'
        ),
        'user_type': fields.String(
            required=True, description='user type'
        )
    }
)
