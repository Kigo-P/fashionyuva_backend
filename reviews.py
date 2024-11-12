from models import Review, db
from flask import Blueprint, make_response, jsonify, request
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

    # a method to post a review
    def post(self):
        #  creating a new review
        data = request.get_json()
        new_review = Review(
            rating=data["rating"],
            comment=data["comment"],
            user_id=data["user_id"],
            product_id=data["product_id"],
        )

        #  adding and commiting the new review to the database
        db.session.add(new_review)
        db.session.commit()
        #  making the new review to a dictionary using to_dict() method
        new_review_dict = new_review.to_dict()

        #  creating and returning a response
        response = make_response(new_review_dict, 201)
        return response

    pass


# creating a ReviewsById Resource
class ReviewsById(Resource):
    #  a method to get one user
    def get(self, id):
        # querying and filtering the database using the id
        reviews = Review.query.filter_by(id=id).all()
        if review:
            #  creating a review dict using the to_dict method
            review_dict = [review.to_dict() for review in reviews]
            # creating and making a response
            response = make_response(review_dict, 200)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"error": "Review  not found"}
            response = make_response(response_body, 404)
            return response

    #  a method to update a review
    def patch(self, id):
        # querying and filtering the database using the id
        review = Review.query.filter_by(id=id).first()
        if review:
            #  creating a for loop to set the attributes
            data = request.get_json()
            for attr in data:
                setattr(review, attr, data[attr])

            # commiting to the database
            db.session.commit()
            #  making the review to a dictionary using to_dict() method
            review_dict = review.to_dict()
            # creating and making a response
            response = make_response(review_dict, 200)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"error": "Review  not found"}
            response = make_response(response_body, 404)
            return response

    #  a method to delete the review
    def delete(self, id):
        # querying and filtering the database using the id
        review1 = Review.query.filter_by(id=id).first()
        if review1:
            #  deleting the review1 and commiting the changes to the database
            db.session.delete(review1)
            db.session.commit()
            #  creating and returning a response based on the response body
            response_body = {"message": "Review deleted successfully"}
            response = make_response(response_body, 204)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"error": "Review not found"}
            response = make_response(response_body, 404)
            return response


api.add_resource(Reviews, "/reviews", endpoint="reviews")
api.add_resource(ReviewsById, "/reviews/<int:id>", endpoint="/reviews_by_id")
