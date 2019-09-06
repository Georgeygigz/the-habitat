# app/__init__.py
'''
Register Blueprints
'''

from flask_migrate import Migrate
from flask import Flask, Blueprint, make_response, jsonify,
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_jwt_extended import (create_access_token, jwt_required, get_raw_jwt)
import os
import json
from flask_cors import CORS

from app.api.models.databases import db
from flask import Flask, redirect, url_for, render_template, flash
from app.api.utils.helpers.social_auth import SocialAuthentication
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user

# local imports
from instance.config import app_configuration, Config
from app.api.views.rentals.rentals import (ViewProducts, ViewSingleProduct)
from app.api.views.authentication.auth_view import CreateAccount, Login, UpdateUserRole, Logout,SocialLogin
from flask_login import LoginManager
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.google import make_google_blueprint, google


blueprint = Blueprint('product', __name__, url_prefix='/api/v2')
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_configuration[config_name])
    db.init_app(app)
    app.secret_key = "fgvhbjdfsfte468r7yfhidkjbcxsgfdtyghc"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app_api = Api(blueprint)
    app.register_blueprint(blueprint)

    app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    google_bp = make_google_blueprint(offline=True, scope=["profile", "email"])
    app.register_blueprint(google_bp, url_prefix="/google_login")

    app.config['JWT_SECRET_KEY'] = "dbskbjdmsdscdscdsdk"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2400)
    jwt.init_app(app)
    CORS(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    app_api.add_resource(ViewProducts, '/products')
    app_api.add_resource(ViewSingleProduct, '/products/<int:product_id>')
    app_api.add_resource(CreateAccount, '/auth/register')
    app_api.add_resource(Login, '/auth/login')
    app_api.add_resource(UpdateUserRole, '/auth/role/<int:user_id>')
    app_api.add_resource(Logout, '/auth/logout')
    app_api.add_resource(SocialLogin, '/github_login')


    @app.route('/github_login')
    def post():
        if not github.authorized:
            return redirect(url_for("github.login"))
        resp = github.get("/user")
        token = create_access_token(identity=resp.json()['email'])
        return make_response(jsonify({"message": "Login succesful", "token": token}))

    @app.route("/google_login")
    def index():
        if not google.authorized:
            return redirect(url_for("google.login"))
        resp = google.get("/oauth2/v1/userinfo")
        assert resp.ok, resp.text
        return "{email}".format(email=resp.json())

    @app.route('/home')
    def home_page():
        return make_response(jsonify({
            "message": "this is home page"
        }))

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
    return app
