from models import Category, db
from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError

category = Blueprint("category", __name__)
api = Api(category)


class Categories(Resource):

    def get(self):
        try:

            categories = Category.query.all()
            if categories:

                category_dict = [category.to_dict() for category in categories]

                response = make_response(category_dict, 200)
                return response
            else:
                response_body = {"message": "No categories found"}
                response = make_response(response_body, 404)
                return response
        except SQLAlchemyError as e:

            response_body = {"message": f"Database error: {str(e)}"}
            response = make_response(response_body, 500)
            return response
        except Exception as e:

            response_body = {"message": f"An unexpected error occurred: {str(e)}"}
            response = make_response(response_body, 500)
            return response

    def post(self):
        try:

            data = request.get_json()
            if not data or not data.get("name") or not data.get("description"):
                response_body = {
                    "message": "Missing required fields: name and description are required"
                }
                response = make_response(response_body, 400)
                return response

            new_category = Category(
                name=data["name"],
                description=data["description"],
            )

            db.session.add(new_category)
            db.session.commit()

            new_category_dict = new_category.to_dict()
            response = make_response(new_category_dict, 201)
            return response
        except SQLAlchemyError as e:

            response_body = {"message": f"Database error: {str(e)}"}
            response = make_response(response_body, 500)
            return response
        except Exception as e:

            response_body = {"message": f"An unexpected error occurred: {str(e)}"}
            response = make_response(response_body, 500)
            return response


class CategoriesById(Resource):

    def get(self, id):
        try:

            category = Category.query.filter_by(id=id).first()
            if category:

                category_dict = category.to_dict()
                response = make_response(category_dict, 200)
                return response
            else:

                response_body = {"message": "Category not found"}
                response = make_response(response_body, 404)
                return response
        except SQLAlchemyError as e:

            response_body = {"message": f"Database error: {str(e)}"}
            response = make_response(response_body, 500)
            return response
        except Exception as e:

            response_body = {"message": f"An unexpected error occurred: {str(e)}"}
            response = make_response(response_body, 500)
            return response

    def patch(self, id):
        try:

            category = Category.query.filter_by(id=id).first()
            if category:
                data = request.get_json()
                if not data:
                    response_body = {"message": "No data provided for update"}
                    response = make_response(response_body, 400)
                    return response

                for attr in data:
                    setattr(category, attr, data[attr])

                db.session.commit()

                category_dict = category.to_dict()
                response = make_response(category_dict, 200)
                return response
            else:

                response_body = {"message": "Category not found"}
                response = make_response(response_body, 404)
                return response
        except SQLAlchemyError as e:

            response_body = {"message": f"Database error: {str(e)}"}
            response = make_response(response_body, 500)
            return response
        except Exception as e:

            response_body = {"message": f"An unexpected error occurred: {str(e)}"}
            response = make_response(response_body, 500)
            return response

    def delete(self, id):
        try:

            category = Category.query.filter_by(id=id).first()
            if category:

                db.session.delete(category)
                db.session.commit()

                response_body = {"message": "Category deleted successfully"}
                response = make_response(response_body, 204)
                return response
            else:

                response_body = {"message": "Category not found"}
                response = make_response(response_body, 404)
                return response
        except SQLAlchemyError as e:

            response_body = {"message": f"Database error: {str(e)}"}
            response = make_response(response_body, 500)
            return response
        except Exception as e:

            response_body = {"message": f"An unexpected error occurred: {str(e)}"}
            response = make_response(response_body, 500)
            return response


api.add_resource(Categories, "/categories", endpoint="categories")
api.add_resource(CategoriesById, "/categories/<int:id>", endpoint="categories_by_id")
