# import the function that will return an instance of a connection
from mysqlconnection import connectToMySQL
# model the class after the user table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        
    # Now we use class methods to query our database
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('users_schema').query_db(query)
        # Create an empty list to append our instances of users
        users = []
        # Iterate over the db results and create instances of users with cls.
        for one_record in results:
            users.append( cls(one_record) )
        return users
            
    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('users_schema').query_db(query, data)
        
        return cls( results[0] )
    
    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO users ( first_name , last_name , email , created_at, updated_at ) VALUES ( %(fname)s , %(lname)s , %(email)s , NOW(), NOW());"
        return connectToMySQL('users_schema').query_db( query, data )


    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        results = connectToMySQL('users_schema').query_db(query, data)
        return

    @classmethod
    def update_user(cls, data):
        # print(data[fname'])
        query = "UPDATE users SET first_name =%(fname)s, last_name = %(lname)s, email = %(email)s, created_at = now(), updated_at = now() WHERE id = %(user_id)s;"
        
        return connectToMySQL('users_schema').query_db( query, data )
