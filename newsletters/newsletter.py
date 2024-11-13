from models import Newsletter,db
from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource

newsletter = Blueprint("newsletter", __name__)
api = Api(newsletter)

class Newsletters(Resource):
    #  a method to get all newsletter
    def get(self):
        # querying the database to get a list of all the newsletters
        newsletters = Newsletter.query.all()
        # Looping through newsletters and getting a user as a dictionary using to_dict() method
        newsletter_dict = [newsletter.to_dict() for newsletter in newsletters]
        # creating and making a response
        response = make_response(newsletter_dict, 200)
        return response
    
    # a method to post an newsletter
    def post(self):
        #  creating a new newsletter
        data = request.get_json()
        new_newsletter = Newsletter(
            email = data["email"],
        )

        #  adding and commiting the new newsletter to the database
        db.session.add(new_newsletter)
        db.session.commit()

        #  making new_newsletter to a dictionary
        new_newsletter_dict = new_newsletter.to_dict()
        #  creating and returning a response
        response = make_response(new_newsletter_dict, 201)
        return response
    pass

# creating a NewslettersById Resource
class NewslettersById(Resource):
    #  a method to get one newsletter
    def get(self,id):
        # querying and filtering the database using the id
        newsletter = Newsletter.query.filter_by(id=id).first()
        if newsletter:
            #  creating a newsletter dict using the to_dict method
            newsletter_dict = newsletter.to_dict()
            # creating and making a response
            response = make_response(newsletter_dict, 200)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"message":"Newsletter not found"}
            response = make_response(response_body, 404)
            return response
    
    #  a method to update an newsletter
    def patch(self, id):
        # querying and filtering the database using the id
        newsletter = Newsletter.query.filter_by(id=id).first()
        if newsletter:
            data = request.get_json()
            #  creating a for loop to set the attributes
            for attr in data:
                setattr(newsletter, attr, data[attr])
            
            # commiting to the database
            db.session.commit()
            #  making newsletter to a dictionary
            newsletter_dict = newsletter.to_dict()
            response = make_response(newsletter_dict, 200)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"message":"Newsletter not found"}
            response = make_response(response_body, 404)
            return response
    
    #  a method to delete the newsletter
    def delete(self, id):
        newsletter = Newsletter.query.filter_by(id=id).first()
        if newsletter:
            db.session.delete(newsletter)
            db.session.commit()

            #  creating and returning a response based on the response body
            response_body = {"message":"Newsletter deleted successfully"}
            response = make_response(response_body, 204)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"error": "Newsletter not found"}
            response = make_response(response_body, 404)
            return response

    pass

api.add_resource(Newsletters, "/newsletters", endpoint="newsletters")
api.add_resource(NewslettersById, "/newsletters/<int:id>",endpoint="newsletters_by_id" )