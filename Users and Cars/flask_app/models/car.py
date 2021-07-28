from flask_app import app
# import re  # the regex module
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


class Car:
    def __init__(self, data):
        self.id = data['id']
        self.color = data['color']
        self.seats = data['seats']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.driver = {}

    @staticmethod
    def validate_car(data):
        is_valid = True
        if len(data['color']) < 3 or len(data['color']) > 25:
            flash("Color must be between 3 and 25 character long!")
            is_valid = False
        if not data['seats']:
            flash("Please enter a number for numner of seates!")
            is_valid = False

        elif int(data['seats']) > 15:
            flash("Number of seats cannot exceed 15!")
            is_valid = False
        return is_valid

    @classmethod
    def save_car(cls, data):
        query = "INSERT INTO cars (color, seats, user_id, created_at, updated_at) values(%(color)s,%(seats)s,%(driver_id)s, NOW(), NOW());"
        results = connectToMySQL('login_user').query_db(query, data)
        return results

    @classmethod
    def all_cars(cls):
        query = "SELECT * FROM cars JOIN users ON users.id = user_id;"
        results = connectToMySQL('login_user').query_db(query)

        cars = []
        for row_in_db in results:
            one_car = cls(row_in_db)

            user_data = {
                'id': row_in_db['users.id'],
                'first_name': row_in_db['first_name'],
                'last_name': row_in_db['last_name'],
                'email': row_in_db['email'],
                'password': row_in_db['password'],
                'created_at': row_in_db['users.created_at'],
                'updated_at': row_in_db['users.updated_at']

            }

            one_car.driver = User(user_data)
            cars.append(one_car)
        return cars

    @classmethod
    def get_car_info(cls, data):
        query = "SELECT * FROM cars JOIN users ON users.id = user_id WHERE cars.id = %(id)s;"
        results = connectToMySQL('login_user').query_db(query, data)

        one_car = cls(results[0])

        user_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']

        }
        one_car.driver = User(user_data)
        return one_car

    @classmethod
    def update_car(cls, data):
        query = "UPDATE cars SET color =%(color)s,seats = %(seats)s, updated_at = NOW() WHERE id = %(id)s;"

        results = connectToMySQL('login_user').query_db(query, data)

    @classmethod
    def eliminate_car(cls, data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        results = connectToMySQL('login_user').query_db(query, data)
        return
