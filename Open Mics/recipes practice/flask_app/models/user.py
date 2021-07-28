from flask_app import app
import re  # the regex module
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("The first name should be at least 2 characters long!!")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("The last name should be at least 2 characters long!!")
            is_valid = False
        if len(data['password']) < 8:
            flash("The password should be at least 8 characters long!!")
            is_valid = False
        if data['password'] != data['conf_pass']:
            flash("Password and Confirmation Password did not match!!")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Provide a valid email!!")
            is_valid = False
        return is_valid

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s, NOW(), NOW());"

        results = connectToMySQL('openmics_schema').query_db(query, data)
        return results


    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("openmics_schema").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])


    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("openmics_schema").query_db(query, data)
        return cls(result[0])
