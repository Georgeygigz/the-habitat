"""This is where all authentication Endpoints will be captured."""
import re
from flask_jwt_extended import (create_access_token, jwt_required,get_raw_jwt)
from flask import request, jsonify, make_response
import datetime
from functools import wraps
from passlib.hash import sha256_crypt
from flask_restful import Resource, reqparse
from flask_dance.contrib.github import github
from flask_dance.contrib.google import google

from flask import Flask, redirect, url_for, render_template, flash


from app.api.models.auth_modles import User;
from app.api.schemas.auth_shema import UserSchema
from app.api.utils.validators import check_user_if_exist,check_valid_email,check_valid_password
from app.api.utils.authorization import admin_required
blacklist = set()

from instance.config import AppConfig


class CreateAccount(Resource):
    """Create a new account."""
    @jwt_required
    @admin_required
    @check_user_if_exist
    @check_valid_email
    @check_valid_password
    def post(self):
        """Create an account for new user."""
        users = User.query.all()
        data = request.get_json(force=True)
        user_id =  2
        username = data["username"]
        email = data["email"]
        password = data["password"]
        user_type = data["user_type"]
        current_user = [user for user in users if user.email == email]

        new_user_detail = {"user_id": len(users)+1,
                           "username": username,
                           "email": email,
                           "password": sha256_crypt.hash(password),
                           "user_type": user_type}
        schema  = UserSchema()

        data1 = schema.load_object_into_schema(new_user_detail)
        new_data = User(**data1)
        new_data.save()
        return make_response(
                jsonify({"message": "Account created successfuly"}), 201)#created


class Login(Resource):
    """Login Endpoint."""

    def post(self):
        data = request.get_json(force=True)
        email = data['email']
        get_password = data['password']
        cur_user = User.query.filter(User.email==email).first()

        if cur_user:
            password = cur_user.password
            if sha256_crypt.verify(get_password, password):
                token = create_access_token(identity=cur_user.email)
                result = {"message": "Login succesful", "token": token}

            else:
                return make_response(
                    jsonify({"message": "Incorrect Password"}), 401)#unauthorized
        else:
            return make_response(
                jsonify({"message": "Incorrect Email. If have not account, contact Admin"}), 401)#unauthorized

        return result, 200 #ok

class SocialLogin(Resource):
    def get(self):
        if not google.authorized:
            return redirect(url_for("google.login"))
        resp = google.get("/oauth2/v1/userinfo")
        assert resp.ok, resp.text
        return "{email}".format(email=resp.json())

class UpdateUserRole(Resource):
    @jwt_required
    @admin_required
    def put(self, user_id):
        """Update user role."""
        users = Users().get_all_users()
        data = request.get_json(force=True)
        role = (data["role"]).lower()
        current_user = User.query.filter(User.user_id==user_id).first()
        # update_user = [user for user in users if user['user_id'] == user_id]
        if not current_user:
            return make_response(jsonify({'Error': "User Not found"}), 400) #Bad request
        user = Users()
        user.update_user(user_id, role)
        return make_response(jsonify(
            {'Message': "{} Updated Successfuly".format(current_user.username)}), 200) #ok

class Logout(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return make_response(jsonify({"message": "Successfully logged out"}), 200)#ok
        