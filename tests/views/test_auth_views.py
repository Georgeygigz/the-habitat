# app/tests/v1/test_storeviews.py
import unittest
import json
from main import create_app
from tests.base_test import BaseTest

class TestStoreViews(BaseTest):
    def test_create_account(self):
        """Test create a new account."""
        resp=self.user_signup()
        result = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(result['message'], 'Account created successfuly')
        self.assertEqual(resp.status_code, 201)
    
    def test_invalid_email(self):
        """Test for invalid email."""
        resp=self.check_invalid_email()
        result = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(result['message'], 'invalid Email')
        self.assertEqual(resp.status_code, 400)

    def test_invalid_password(self):
        """Test for invalid password."""
        resp=self.check_invalid_password()
        result = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(result['message'], 'invalid password')
        self.assertEqual(resp.status_code, 400)

    def test_user_login(self):
        """Test Login."""
        response = self.check_login()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200,result['message'])

    def test_add_existing_user(self):
        """Test add existing account."""
        resp=self.signup_existing_user()
        result = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(result['message'], 'hellem@gmail.com Already Exist')
        self.assertEqual(resp.status_code, 409)
    
    def test_user_login_with_invalid_password(self):
        """Test Login with invalid password"""
        response = self.login_with_invalid_password()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'],'Incorrect Password')
        self.assertEqual(response.status_code, 401,result['message'])
    
    def test_user_login_with_invalid_email(self):
        """Test Login with invalid email."""
        response = self.login_with_invalid_email()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'],'Incorrect Email. If have not account, contact Admin')
        self.assertEqual(response.status_code, 401)
 