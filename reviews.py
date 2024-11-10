from models import Review
from flask import Blueprint, make_response, jsonify
from flask_restful import Api, Resource

review = Blueprint("review", __name__)
api = Api(review)

# Creating a Reviews Resource
class Reviews(Resource):
    #  a method to get all reviews
    def get(self):
        # querying the database to get a list of all the reviews
        reviews = Review.query.all()
        # Looping through reviews and getting a user as a dictionary using to_dict() method
        review_dict = [review.to_dict() for review in reviews]
        # creating and making a response
        response = make_response(review_dict, 200)
        return response

api.add_resource(Reviews, "/reviews", endpoint="reviews")