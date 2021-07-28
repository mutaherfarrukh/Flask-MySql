from flask_app import app
# import re  # the regex module
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
# from flask_app.models import user

class Openmic:
    def __init__(self, data):
        self.id = data['id']
        self.venue = data['venue']
        self.type = data['type']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.description = data['description']
        self.date = data['date']

        self.user = {}

    @staticmethod  # 1.iii next steps for validation after 1.ii
    # this validation is for create_openmic venue, type, date, decription requirement.
    def validate_openmic(data):
        is_valid = True
        if len(data['venue']) < 4:
            flash("Venue must be atleast 4 character long!")
            is_valid = False

        if len(data['type']) < 2:
            flash("Type must be atleast 2 character long!")
            is_valid = False

        if len(data['date']) < 6:
            flash("Date must be atleast 6 character long!")
            is_valid = False

        if len(data['description']) < 10:
            flash("Description must be atleast 10 character long!")
            is_valid = False
        return is_valid


    @classmethod
    def save(cls, data):
        query = "INSERT INTO openmics (venue, type, date, description, user_id, created_at, updated_at) VALUES(%(venue)s,%(type)s,%(date)s,%(description)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL('openmics_schema').query_db(query, data)

    @classmethod
    def all_openmics(cls):
        query = "SELECT * FROM openmics;"
        results = connectToMySQL('openmics_schema').query_db(query)
        openmics = []
        for one_openmic in results:
            openmics.append(cls(one_openmic))
            return openmics

    @classmethod
    def one_openmic(cls, data):
        query = "SELECT * FROM openmics JOIN users ON users.id = user_id WHERE openmics.id = %(id)s"
        results = connectToMySQL('openmics_schema').query_db(query, data)

        openmic = cls(results[0])

        user_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']

        }
        openmic.posted_by = User(user_data)
        return openmic


    @classmethod
    def update_one_openmic(cls, data):
        query = "UPDATE openmics SET venue =%(venue)s, description = %(description)s, date = %(date)s, created_at = now(), updated_at = now(), type = %(type)s WHERE id = %(id)s;"
        return connectToMySQL('openmics_schema').query_db( query, data )




    @classmethod
    def get_openmic_info(cls, data):
        query = "SELECT * FROM openmics JOIN users ON users.id = user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('openmics_schema').query_db(query, data)

        one_openmic = cls(results[0])

        user_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']
        }
        one_openmic.user = User(user_data)
        return one_openmic



    @classmethod
    def delete_openmic(cls, data):
        query = "DELETE FROM openmics WHERE id = %(id)s;"
        results = connectToMySQL('openmics_schema').query_db(query, data)
        return results


    @classmethod
    def get_one_openmic(cls, data):
        query = "SELECT * FROM openmics WHERE id = %(id)s;"
        
        results = connectToMySQL('openmic_schema').query_db(query, data)
        return cls( results[0] )

