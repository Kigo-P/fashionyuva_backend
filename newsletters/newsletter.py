from models import Newsletter, db
from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

newsletter = Blueprint("newsletter", __name__)
api = Api(newsletter)


class Newsletters(Resource):
    def get(self):
        try:
            newsletters = Newsletter.query.all()
            newsletter_dict = [newsletter.to_dict() for newsletter in newsletters]
            return make_response(jsonify(newsletter_dict), 200)
        except SQLAlchemyError as e:
            return make_response(
                {"message": "An error occurred while retrieving newsletters."}, 500
            )

    def post(self):
        try:
            data = request.get_json()

            if "email" not in data:
                return make_response({"message": "Email is required."}, 400)

            existing_newsletter = Newsletter.query.filter_by(
                email=data["email"]
            ).first()
            if existing_newsletter:
                return make_response(
                    {"message": "This email is already subscribed."}, 400
                )

            new_newsletter = Newsletter(email=data["email"])
            db.session.add(new_newsletter)
            db.session.commit()

            new_newsletter_dict = new_newsletter.to_dict()
            return make_response(jsonify(new_newsletter_dict), 201)

        except IntegrityError:
            db.session.rollback()
            return make_response({"message": "Database integrity error occurred."}, 500)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(
                {"message": "An error occurred while processing your request."}, 500
            )
        except Exception as e:
            return make_response(
                {"message": f"An unexpected error occurred: {str(e)}"}, 500
            )


class NewslettersById(Resource):

    def get(self, id):
        try:
            newsletter = Newsletter.query.filter_by(id=id).first()
            if newsletter:
                newsletter_dict = newsletter.to_dict()
                return make_response(jsonify(newsletter_dict), 200)
            else:
                return make_response({"message": "Newsletter not found."}, 404)
        except SQLAlchemyError as e:
            return make_response(
                {"message": "An error occurred while retrieving the newsletter."}, 500
            )

    def patch(self, id):
        try:
            newsletter = Newsletter.query.filter_by(id=id).first()
            if not newsletter:
                return make_response({"message": "Newsletter not found."}, 404)

            data = request.get_json()
            for attr in data:
                if hasattr(newsletter, attr):
                    setattr(newsletter, attr, data[attr])
                else:
                    return make_response({"message": f"Invalid attribute: {attr}"}, 400)

            db.session.commit()
            newsletter_dict = newsletter.to_dict()
            return make_response(jsonify(newsletter_dict), 200)

        except IntegrityError:
            db.session.rollback()
            return make_response({"message": "Database integrity error occurred."}, 500)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(
                {"message": "An error occurred while updating the newsletter."}, 500
            )
        except Exception as e:
            return make_response(
                {"message": f"An unexpected error occurred: {str(e)}"}, 500
            )

    def delete(self, id):
        try:
            newsletter = Newsletter.query.filter_by(id=id).first()
            if not newsletter:
                return make_response({"message": "Newsletter not found."}, 404)

            db.session.delete(newsletter)
            db.session.commit()
            return make_response({"message": "Newsletter deleted successfully."}, 204)

        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(
                {"message": "An error occurred while deleting the newsletter."}, 500
            )
        except Exception as e:
            return make_response(
                {"message": f"An unexpected error occurred: {str(e)}"}, 500
            )


api.add_resource(Newsletters, "/newsletters", endpoint="newsletters")
api.add_resource(NewslettersById, "/newsletters/<int:id>", endpoint="newsletters_by_id")
