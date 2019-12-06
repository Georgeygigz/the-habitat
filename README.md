# The Habitat
This is a plat form that helps tenants find the house to rent in a more efficient way

[![CircleCI](https://circleci.com/gh/Georgeygigz/the-habitat/tree/develop.svg?style=svg)](https://circleci.com/gh/Georgeygigz/the-habitat/tree/develop) [![Coverage Status](https://coveralls.io/repos/github/Georgeygigz/the-habitat/badge.svg?branch=develop)](https://coveralls.io/github/Georgeygigz/the-habitat?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/b5d06a15a2f52386c419/maintainability)](https://codeclimate.com/github/Georgeygigz/the-habitat/maintainability)


# This project creates a set of API Endpoints listed below
| EndPoints       | Functionality  | HTTP Method  |
| ------------- |:-------------:| -----:|
| api/v1/auth/register|Create user account|POST|
| api/v1/auth/login|User login |POST|
| api/v1/auth/role|Update user role login |PUT|

## TOOLS TO BE USED IN THE CHALLENGE
1. Server-Side Framework:[Flask Python Framework](http://flask.pocoo.org/)
2. Linting Library:[Pylint, a Python Linting Library](https://www.pylint.org/)
3. Style Guide:[PEP8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
4. Testing Framework:[PyTest, a Python Testing Framework](https://docs.pytest.org/en/latest/)
5. Testing Endpoints: [PostMan](https://www.getpostman.com/)

**How to run the application**
 1. Make a new directory on your computer
 2. Open the terminal and navigate to the folder
 3. `git clone` this  <code>[repo](https://github.com/Georgeygigz/store-manager-api/)</code>
 4.  run `pip install -r requirements.txt` to install the dependencies
 5.  run `python manage.py db upgrade` to upgrade the database
 6.  run `python manage.py db migrate` to make migration
 7.  Create a virtual environment
 8.  Export the environmental variable
 9.  Then on your terminal write ```flask run``` to start the server
 10. Then on [postman](https://www.getpostman.com/), navigate to this url `api/v1/auth/login`


# heroku application Link

# View on postman documentation

# Author
`Georgey Gigz`

# Realease 
 Version one `(v1)`
