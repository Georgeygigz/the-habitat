# app/__init__.py
'''
Register Blueprints
'''

from flask_migrate import Migrate
from flask import Flask, Blueprint,make_response,jsonify
from flask_restplus import Api, fields
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from instance.config import app_configuration, Config
from flask_cors import CORS

from api.models.databases import db


# local imports
from api import api_blueprint
from instance.config import app_configuration
# from api.views.rentals.rentals import (ViewProducts, ViewSingleProduct)
# from api.views.authentication.auth_view import CreateAccount, Login,UpdateUserRole, Logout

app_api = Api(api_blueprint,version='1.0.0', title='The Habitat',
    description='The habitat API documentation', 
    default='The habitat', default_label='The habitat',doc='/doc/' )
jwt = JWTManager()

def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_configuration[config_name])
    db.init_app(app)

    app.register_blueprint(api_blueprint)
    app.config['JWT_SECRET_KEY'] = "dbskbjdmsdscdscdsdk"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2400)
    jwt.init_app(app)
    CORS(app)
    
    @app.errorhandler(404)
    def not_found(e):
        # defining function
        return make_response(jsonify({
            "Message": "Route not found. Please check on the route"
        }), 404)

    @app.errorhandler(500)
    def internal_error(e):
        return make_response(jsonify({
            "Message": "Internal server"
        }), 500)
        
    import api.views

    return app
