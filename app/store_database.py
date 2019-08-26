#store_database.py

"""Create new connection"""
import psycopg2
import os
from instance.config import app_configuration

dev_url=app_configuration['development'].SQLALCHEMY_DATABASE_URI
# dev_url = 'postgres://test-user@localhost:5432/test-db'

def conn_db():
	"""Create a new connection."""
	conn=psycopg2.connect(dev_url)
	return conn
