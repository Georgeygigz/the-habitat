from marshmallow import fields, post_load, pre_load, Schema
from api.utils.validation_error import ValidationError

from api.models.auth_modles import User
from .base_schema import BaseSchema


class ProductsSchema(BaseSchema):
    product_id = fields.Int()
    product_name = fields.Str()
    category_id = fields.Int()
    stock_amount = fields.Float()
    price = fields.Float()
    low_inventory_stock = fields.Float()

