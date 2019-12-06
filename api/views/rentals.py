# app/api/v1/views/store_views.py

"""This is where all API Endpoints will be captured."""
from flask import request, jsonify, make_response
from datetime import date
from flask_restplus import Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)

# local imports
from api.utils.authorization import (
    admin_required, store_attendant_required)

from api.models.products_model import Products
from api.schemas.products_schema import ProductsSchema
from utilities.swagger.collections.rentals import rental_namespace

def get_products():
    products = Products.query.all()
    return products

@rental_namespace.route('')
class ViewProducts(Resource):
    @jwt_required
    def get(self):
        """Get all products."""
        products = get_products()
        schema  = ProductsSchema(many=True)
        data = schema.dump(products)
        if not products:
            return make_response(
                jsonify({"message": "No Available products"}), 200) #Ok
        return make_response(jsonify({"Available Products": data}), 200) #Ok

    @jwt_required
    @admin_required
    def post(self):
        """Add a new product."""
        products = get_products()
        data = request.get_json(force=True)
        product_id = len(products) + 1
        product_name = data["product_name"]
        category = data["category_id"]
        stock_amount = data["stock_amount"]
        price = data['price']
        inventory_stock = data['low_inventory_stock']


        product = [product for product in products if product.product_name
                   == request.json['product_name']]

        if (not request.json or "product_name" not in request.json):
            return make_response(jsonify({'Error': "Request Not found"}), 404)# Not Found

        if type(request.json['stock_amount'])not in [int, float]:
            return make_response(
                jsonify({"Error": "Require int or float type"}))

        new_product = {
            "product_id": product_id,
            "product_name": product_name,
            "category_id": category,
            "stock_amount": stock_amount,
            "price": price,
            "low_inventory_stock": inventory_stock
        }

        product_schema = ProductsSchema()
        new_product_detail = product_schema.load_object_into_schema(new_product)
        new_pro = Products(**new_product_detail)
        new_pro.save()
        return make_response(jsonify({"New Product": new_product}), 201) #Created

@rental_namespace.route('/<int:product_id>')
class ViewSingleProduct(Resource):
    @jwt_required
    def get(self, product_id):
        """Fetch single product."""
        products = get_products()
        single_product = [
            product for product in products if product.product_id == product_id]
        schema  = ProductsSchema(many=True)
        data = schema.dump(single_product)
        if not single_product:
            return make_response(jsonify({"Error": "Product Not Found"}), 400) #Bad Request
        return make_response(jsonify({"Product": data}), 200)  # ok

    @jwt_required
    @admin_required
    def put(self, product_id):
        """Update product."""
        products = get_products()
        data = request.get_json(force=True)
        product_name = (data["product_name"]).lower()
        category_id = data["category_id"]
        stock_amount = data["stock_amount"]
        price = data['price']
        low_inventory_stock = data['low_inventory_stock']

        product = [
            product for product in products if product.product_id == product_id]
        if not product:
            return make_response(jsonify({'Error': "Product Not found"}),  400) #Bad Request
        product[0].product_name=product_name
        product[0].category_id=category_id
        product[0].stock_amount=stock_amount
        product[0].price=price
        product[0].low_inventory_stock=low_inventory_stock
        product[0].save()
        return make_response(jsonify(
            {'Message': "{} Updated Successfully".format(product[0].product_name)}), 200)#Ok

    @jwt_required
    @admin_required
    def delete(self, product_id):
        """Delete product."""
        products = get_products()
        product = [
            product for product in products if product.product_id == product_id]
        if not product:
            return make_response(jsonify({'Error': "Product Not found"}),  400) #Bad Request

        product[0].delete_(product[0])
        return make_response(jsonify({'Message': "Deleted Successfully"}), 200)#ok
