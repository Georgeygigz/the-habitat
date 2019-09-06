# app/tests/v2/base_test.py
import unittest
import json
import jwt
from app import create_app
from instance.config import AppConfig
from app.api.models.databases import db
from app.api.models.auth_modles import User


"""Creating a new testing  class."""
class BaseTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app(AppConfig)
        self.client = self.app.test_client
        self.app.testing = True
        
        with self.app.app_context():
            # create all tables
            db.create_all()
            user_details = {'user_id':1,'username':'mary','email':'hellem@gmail.com','password':'$5$rounds=535000$0wOk78L6sQ6Y/E6T$RmjlaGXrrZksCJSq8spoPpqMEQbSFae/zOMr/VYIHm1','user_type':'admin'}
            new_user = User(**user_details)
            new_user.save()
        
        self.products = {
            "product_id": 1,
            "product_name": "orange",
            "category_id": 1,
            "stock_amount": 2000,
            "price": 20,
            "low_inventory_stock": 2
        }
        self.invalid_data_types_products = {
            "product_id": 1,
            "product_name": "Bread",
            "category_id": 1,
            "stock_amount": "2000",
            "price": 20,
            "low_inventory_stock": 2
        }

        self.sales = {
            "sale_id": 1,
            "attedant_name": "Mary",
            "customer_name": "James",
            "product_name": "orange",
            "product_price": 20,
            "quantity": 3,
            "total_price": 60,
            "date_sold": "12-3-2018"}
        
        self.exeed_sales = {
            "sale_id": 1,
            "attedant_name": "Mary",
            "customer_name": "James",
            "product_name": "orange",
            "product_price": 20,
            "quantity": 3000,
            "total_price": 60,
            "date_sold": "12-3-2018"}

        self.user = {
            "user_id": 1,
            "username": 'marry',
            "email": "marry@gmail.com",
            "password": "maR#@Y_123",
            "user_type": "attedant"
        }
        self.user_invalid_password = {
            "user_id": 1,
            "username": 'marry',
            "email": "marry@gmail.com",
            "password": "manfhf_123",
            "user_type": "attedant"
        }
        self.user_invalid_email= {
            "user_id": 1,
            "username": 'marry',
            "email": "marrymail.com",
            "password": "maR#@Y_123",
            "user_type": "attedant"
        }
        self.admin = {
            "user_id": 1,
            "username": 'george',
            "email": "george@gmail.com",
            "password": "maR#@Y_123",
            "user_type": "Admin"
        }
        self.user1 = {
            "email": "hellem@gmail.com",
            "password": "G@_gigz-2416"
        }
        self.invalid_password = {
            "email": "hellem@gmail.com",
            "password": "g@_gigz-"
        }
        self.invalid_email = {
            "email": "gergey@gmail.com",
            "password": "g@_gigz-2416"
        }
        self.invalid_product_values = {
            "product_id": 1,
            "product_name": "",
            "category_id": 1,
            "stock_amount": 2000,
            "price": 20,
            "low_inventory_stock": 2
        }
       
        self.invalid_login = {
            "email": "mary@gmail.com",
            "password": "maR#@Y_123",
        }
    def user_login(self):
        
        response = self.client().post('/api/v2/auth/login',
                                 data=json.dumps(self.user1))
        result = json.loads(response.data.decode('utf-8'))
        return result

    def admin_login(self):
        response = self.client().post('/api/v2/auth/login',
                                 data=json.dumps({"email": "hellem@gmail.com","password": "G@_gigz-2416"}))
        
        result = json.loads(response.data.decode('utf-8'))
        return result


    def get_user_token(self):
        resp_login = self.user_login()
        token = resp_login.get("token")
        return token

    def get_admin_token(self):
        resp_login = self.admin_login()
        token = resp_login.get("token")
        return token

    def add_new_product(self):
        access_token=self.get_admin_token()
        response = self.client().post(
            '/api/v2/products',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
            data=json.dumps(self.products)
        
        )
        return response
    
    def update_product(self):
        self.add_new_product()
        access_token=self.get_admin_token()
        response = self.client().put(
            '/api/v2/products',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
            data=json.dumps(self.products)
        
        )
        return response

    def get_all_products(self):
        self.add_new_product()
        access_token=self.get_user_token()
        response = self.client().get(
            '/api/v2/products',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token}
        )
        return response

    def get_unexisting_products(self):
        access_token=self.get_user_token()
        response = self.client().get(
            '/api/v2/products',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token}
        )
        return response

    def delete_products(self):
        self.add_new_product()
        access_token=self.get_admin_token()
        response = self.client().delete(
            '/api/v2/products/1',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token}
        )
        return response

    def delete_unexisting_products(self):
        access_token=self.get_admin_token()
        response = self.client().delete(
            '/api/v2/products/1',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token}
        )
        return response
    
    def update_products(self):
        self.add_new_product()
        access_token=self.get_admin_token()
        response = self.client().put(
            '/api/v2/products/1',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
            data=json.dumps(self.products))
        return response    
    
    def check_invalid_data_type(self):
        access_token=self.get_admin_token()
        response = self.client().post(
            '/api/v2/products',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
            data=json.dumps(self.invalid_data_types_products)
        
        )
        return response

    def fetch_single_product(self):
        self.add_new_product()
        access_token=self.get_user_token()
        response = self.client().get(
            '/api/v2/products/1',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
        )
        return response

    def add_new_sale_record(self):
        self.add_new_product()
        access_token=self.get_user_token()
        response = self.client().post(
            '/api/v2/sales',
            data=json.dumps(self.sales),
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
        )
        return response

    def make_sale_of_unexisting_product(self):
        access_token=self.get_user_token()
        response = self.client().post(
            '/api/v2/sales',
            data=json.dumps(self.sales),
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
        )
        return response

    def check_sale_exist(self):
        self.add_new_product()
        self.add_new_sale_record()
        access_token=self.get_user_token()
        response = self.client().post(
            '/api/v2/sales',
            data=json.dumps(self.sales),
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
        )
        return response    

    def make_sale_of_exeding_amount_instock(self):
        self.add_new_product()
        access_token=self.get_user_token()
        response = self.client().post(
            '/api/v2/sales',
            data=json.dumps(self.exeed_sales),
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
        )
        return response

    def get_all_sales(self):
        self.add_new_sale_record()
        access_token=self.get_user_token()
        response = self.client().get(
            '/api/v2/sales',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
        )
        return response

    def fetch_single_sale_record(self):
        self.add_new_sale_record()
        access_token=self.get_admin_token()
        resp = self.client().get(
            '/api/v2/sales/1',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
        )
        return resp

    def items_outof_range_record(self):
        access_token=self.get_admin_token()
        resp = self.client().get(
            '/api/v2/sales/2',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
        )
        return resp

    def invalid_post_product_url(self):
        response = self.client().post(
            '/api/v2/productss/',
            data=json.dumps(self.products),
            headers={'content_type': 'application/json'}
        )
        return response

    def invalid_get_product_url(self):
        response = self.client().get(
            '/api/v2//productss/',
            data=json.dumps(self.products),
            headers={'content_type': 'application/json'}
        )
        return response
    
    def user_signup(self):
        access_token=self.get_admin_token()
        response = self.client().post(
            '/api/v2/auth/register',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
            data=json.dumps(self.user)
        
        )
        return response

    def signup_existing_user(self):
        self.user_signup()
        access_token=self.get_admin_token()
        response = self.client().post(
            '/api/v2/auth/register',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
            data=json.dumps({
            "user_id": 1,
            "username": 'marry',
            "email": "hellem@gmail.com",
            "password": "maR#@Y_123",
            "user_type": "attedant"
        }))
        return response

    def check_invalid_email(self):
        access_token=self.get_admin_token()
        response = self.client().post(
            '/api/v2/auth/register',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
            data=json.dumps(self.user_invalid_email))
        return response

    def check_invalid_password(self):
        access_token=self.get_admin_token()
        response = self.client().post(
            '/api/v2/auth/register',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
            data=json.dumps(self.user_invalid_password))
        return response

    def check_login(self):
        access_token=self.get_admin_token()
        response = self.client().post(
            '/api/v2/auth/login',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
            data=json.dumps(self.user1))
        return response

    def login_with_invalid_password(self):
        access_token=self.get_admin_token()
        response = self.client().post(
            '/api/v2/auth/login',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
            data=json.dumps(self.invalid_password)
        
        )
        return response

    def login_with_invalid_email(self):
        access_token=self.get_admin_token()
        response = self.client().post(
            '/api/v2/auth/login',
            headers={"content_type":'application/json',"Authorization": "Bearer "  + access_token},
            data=json.dumps(self.invalid_email)
        
        )
        return response
    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():

            db.session.remove()
            db.drop_all()
            