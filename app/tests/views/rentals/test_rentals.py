# app/tests/v1/rentals.py
import unittest
import json
import jwt
from app import create_app
from app.tests.base_test import BaseTest

class TestStoreViews(BaseTest):
    def test_config(self):
        """Test configurations."""
        self.assertEqual(self.app.testing, True)  
        
    def test_get_all_products(self):
        """Test get all products."""
        response=self.get_all_products()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200,result['Available Products'] )

    def test_get_unexisting_products(self):
        """Test geet unexisting products."""
        response=self.get_unexisting_products()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['message'],"No Available products")
        self.assertEqual(response.status_code, 200)

    def test_add_new_product(self):
        """Test add new product."""
        response=self.add_new_product()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201, result['New Product'])
    
    def test_invalid_data_types(self):
        """Test invalid data types."""
        response=self.check_invalid_data_type()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['Error'],"Require int or float type")
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_product(self):
        """Test fetch for single product [GET request]."""
        response=self.fetch_single_product()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200, result['Product'])

    def test_delete_product(self):
        """Test delete product."""
        response=self.delete_products()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['Message'],'Deleted Successfully')
        self.assertEqual(response.status_code, 200)

    def test_delete_unexisting_product(self):
        """Test delete unexisting product."""
        response=self.delete_unexisting_products()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['Error'],'Product Not found')
        self.assertEqual(response.status_code, 400)

    def test_update_product(self):
        """Test update product."""
        response=self.update_products()
        result = json.loads(response.data.decode('utf-8'))
        self.assertEqual(result['Message'],'orange Updated Successfully')
        self.assertEqual(response.status_code, 200)