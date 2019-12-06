"""
This module contains rental collection definitions for use by swagger UI
"""

from . import app_api

rental_namespace = app_api.namespace(
    'products',
    description='A collection of user registration endpoints'
)
