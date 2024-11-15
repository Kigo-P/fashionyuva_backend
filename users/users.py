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
        user_dict = [user.to_dict() for user in users]
        # creating and making a response
        response = make_response(user_dict, 200)
        return response

    # a method to post a user
    def post(self):
        #  creating a new user
        data = request.get_json()

        # Validate email format
        if "@" not in data["email"]:
            # creating and returning a response based on the response body
            response_body = {"message": "Please include an '@' in the email address."}
            response = make_response(response_body, 400)
            return response

        # Check if email already exists in the database
        if User.query.filter_by(email=data["email"]).first():
            # creating and returning a response based on the response body
            response_body = {"message": "Email already exists"}
            response = make_response(response_body, 400)
            return response

        #  generating a password hash
        password = generate_password_hash(data["password"])
        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=password,
            contact=data["contact"],
            user_role=data["user_role"],
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


# creating a UserById Resource
class UserById(Resource):
    #  a method to get one user
    def get(self, id):
        # querying and filtering the database using the id
        user = User.query.filter_by(id=id).first()
        if user:
            #  creating a user dict using the to_dict method
            user_dict = user.to_dict()
            # creating and making a response
            response = make_response(user_dict, 200)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"error": "User  not found"}
            response = make_response(response_body, 404)
            return response

    #  a method to update a user
    def patch(self, id):
        # querying and filtering the database using the id
        user = User.query.filter_by(id=id).first()
        if user:
            #  creating a for loop to set the attributes
            data = request.get_json()
            for attr in data:
                setattr(user, attr, data[attr])

            # commiting to the database
            db.session.commit()
            #  making the user to a dictionary using to_dict() method
            user_dict = user.to_dict()
            # creating and making a response
            response = make_response(user_dict, 200)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"message": "User  not found"}
            response = make_response(response_body, 404)
            return response

    #  a method to delete the user
    def delete(self, id):
        # querying and filtering the database using the id
        user1 = User.query.filter_by(id=id).first()
        if user1:
            #  deleting the user1 and commiting the changes to the database
            db.session.delete(user1)
            db.session.commit()
            #  creating and returning a response based on the response body
            response_body = {"message": "user deleted successfully"}
            response = make_response(response_body, 204)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"error": "user not found"}
            response = make_response(response_body, 404)
            return response


api.add_resource(Home, "/", endpoint="home")
api.add_resource(Users, "/users", endpoint="users")
api.add_resource(UserById, "/users/<int:id>", endpoint="/user_by_id")
