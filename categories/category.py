from models import Category, db
from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource
from authentification.auth import allow
from flask_jwt_extended import jwt_required

category = Blueprint("category", __name__)
api = Api(category)

class Categories(Resource):
    #  a method to get all categories
    def get(self):
        # querying the database to get a list of all the categories
        categories = Category.query.all()
        # Looping through categories and getting a user as a dictionary using to_dict() method
        category_dict = [category.to_dict() for category in categories]
        # creating and making a response
        response = make_response(category_dict, 200)
        return response
    
    @jwt_required()
    @allow("admin")
    # a method to post an category
    def post(self):
        #  creating a new category
        data = request.get_json()
        new_category = Category(
            name = data["name"],
            description = data["description"],
        )

        #  adding and commiting the new category to the database
        db.session.add(new_category)
        db.session.commit()

        #  making new_category to a dictionary
        new_category_dict = new_category.to_dict()
        #  creating and returning a response
        response = make_response(new_category_dict, 201)
        return response
    pass

# creating a CategoriesById Resource
class CategoriesById(Resource):
    #  a method to get one category
    def get(self,id):
        # querying and filtering the database using the id
        category = Category.query.filter_by(id=id).first()
        if category:
            #  creating a category dict using the to_dict method
            category_dict = category.to_dict()
            # creating and making a response
            response = make_response(category_dict, 200)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"message":"Category not found"}
            response = make_response(response_body, 404)
            return response
    
    @jwt_required()
    @allow("admin")
    #  a method to update an category
    def patch(self, id):
        # querying and filtering the database using the id
        category = Category.query.filter_by(id=id).first()
        if category:
            data = request.get_json()
            #  creating a for loop to set the attributes
            for attr in data:
                setattr(category, attr, data[attr])
            
            # commiting to the database
            db.session.commit()
            #  making category to a dictionary
            category_dict = category.to_dict()
            response = make_response(category_dict, 200)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"message":"Category not found"}
            response = make_response(response_body, 404)
            return response
    
    @jwt_required()
    @allow("admin")
    #  a method to delete the category
    def delete(self, id):
        category = Category.query.filter_by(id=id).first()
        if category:
            db.session.delete(category)
            db.session.commit()

            #  creating and returning a response based on the response body
            response_body = {"message":"Category deleted successfully"}
            response = make_response(response_body, 204)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"error": "Category not found"}
            response = make_response(response_body, 404)
            return response

    pass

api.add_resource(Categories, "/categories", endpoint="categories")
api.add_resource(CategoriesById, "/categories/<int:id>",endpoint="categories_by_id" )