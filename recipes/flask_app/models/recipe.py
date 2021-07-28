from flask_app import app
# import re  # the regex module
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User



class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.under30min = data['under30min']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.instruction = data['instruction']
        self.description = data['description']

        self.user = {}

    @classmethod
    def all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_schema').query_db(query)

        recipes = []
        for row_in_db in results:
            one_recipe = cls(row_in_db)

            recipes.append(one_recipe)
        return recipes




    # # Now we use class methods to query our database
    # @classmethod
    # def get_all_recipes(cls):
    #     query = "SELECT * FROM recipes;"
    #     # make sure to call the connectToMySQL function with the schema you are targeting.
    #     results = connectToMySQL('recipes_schema').query_db(query)
    #     # Create an empty list to append our instances of users
    #     recipes = []
    #     # Iterate over the db results and create instances of users with cls.
    #     for one_record in results:
    #         recipes.append( cls(one_record) )
    #     return recipes

    # @classmethod
    # def get_one_recipe(cls, data):
    #     query = "SELECT * FROM recipes WHERE id = %(id)s;"
    #     results = connectToMySQL('recipes_schema').query_db(query, data)
        
    #     return cls( results[0] )
    


    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes ( name , description , instruction , updated_at, under30min, user_id) VALUES ( %(name)s , %(description)s , %(instruction)s , NOW(), %(under30min)s, %(user_id)s);"
        results =  connectToMySQL('recipes_schema').query_db( query, data )
        return results

    @classmethod
    def update_recipe(cls, data):
        # print(data[fname'])
        query = "UPDATE recipes SET name =%(name)s, description = %(description)s, instruction = %(instruction)s, created_at = now(), updated_at = now(), under30min = %(under30min)s WHERE id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db( query, data )

    @classmethod
    def get_recipe_info(cls, data):
        query = "SELECT * FROM recipes JOIN users ON users.id = user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query, data)

        one_recipe = cls(results[0])

        user_data = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': results[0]['password'],
            'created_at': results[0]['users.created_at'],
            'updated_at': results[0]['users.updated_at']

        }
        one_recipe.user = User(user_data)
        return one_recipe


    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        
        return cls( results[0] )



    @classmethod
    def eliminate_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return



    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3 or len(data['name']) > 25:
            flash("Name must be between 3 and 25 character long!")
            is_valid = False
        if not len(data['description']):
            flash("Please enter Description!")
            is_valid = False

        if not len(data['instruction']):
            flash("Please enter Instructions!")
            is_valid = False
        return is_valid

