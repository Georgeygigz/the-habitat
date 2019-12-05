"""
This module contains auth collection definitions for use by swagger UI
"""

from . import app_api

register_namespace = app_api.namespace(
    'auth',
    description='A collection of user registration endpoints'
)
