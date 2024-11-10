from models import User, db
from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash

users = Blueprint("users", __name__)
api = Api(users)

# creating a Home Resource
class Home(Resource):
    def get(self):
        #  creating and returning a response based on the response body
        response_body = {"Message": "Welcome to Fashionyuva"}
        response = make_response(response_body, 200)
        return response
    
# Creating a Users Resource
class Users(Resource):
    #  a method to get all users
    def get(self):
        # querying the database to get a list of all the users
        users = User.query.all()
        # Looping through users and getting a user as a dictionary using to_dict() method
        user_dict = [user.to_dict(rules = ("-address", "-carts", "-orders", "-reviews", "-contactus")) for user in users]
        # creating and making a response
        response = make_response(user_dict, 200)
        return response
    
    # a method to post a user
    def post(self):
        #  creating a new user
        data = request.get_json()
        #  generating a password hash
        password = generate_password_hash(data["password"])
        new_user = User(
            first_name = data["first_name"],
            last_name = data["last_name"],
            email = data["email"],
            password = password,
            contact = data["contact"],
            user_role = data["user_role"]
        )

        #  adding and commiting the new user to the database
        db.session.add(new_user)
        db.session.commit()
        #  making the new user to a dictionary using to_dict() method
        new_user_dict = new_user.to_dict()

        #  creating and returning a response
        response = make_response(new_user_dict, 201)
        return response
    pass

api.add_resource(Home, "/", endpoint="home")
api.add_resource(Users, "/users", endpoint="users")