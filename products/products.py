from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource
from psycopg2 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from models import Product, db, Category, Image
from authentification.auth import allow
from flask_jwt_extended import jwt_required


products = Blueprint("products", __name__)
api = Api(products)


class Products(Resource):
    def get(self):
        try:
            products = Product.query.all()
            return make_response(
                jsonify([product.to_dict() for product in products]), 200
            )
        except SQLAlchemyError as e:
            return make_response(
                jsonify({"message": "Error fetching products", "error": str(e)}), 500
            )

    @jwt_required()
    @allow("admin")
    def post(self):
        data = request.get_json()
        try:
            category_name = data.get("category")
            if category_name:
                category = Category.query.filter_by(name=category_name).first()
                if not category:
                    category = Category(name=category_name)
                    db.session.add(category)
                    db.session.commit()
                category_id = category.id
            else:
                category_id = data.get("category_id")

            new_product = Product(
                title=data["title"],
                description=data["description"],
                price=data["price"],
                size=data["size"],
                color=data["color"],
                material=data["material"],
                quantity=data.get("quantity", 0),
                category_id=category_id,
            )
            db.session.add(new_product)
            db.session.commit()

            images = data.get("images", [])
            for image_url in images:
                new_image = Image(url=image_url, product_id=new_product.id)
                db.session.add(new_image)
            db.session.commit()

            return make_response(jsonify(new_product.to_dict()), 201)

        except IntegrityError:
            db.session.rollback()
            return make_response(
                jsonify({"message": "Product already exists or invalid input"}), 400
            )
        except KeyError as e:
            db.session.rollback()
            return make_response(
                jsonify({"message": f"Missing required field: {str(e)}"}), 400
            )
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(
                jsonify({"message": "Database error occurred", "error": str(e)}), 500
            )
        except Exception as e:
            db.session.rollback()
            return make_response(
                jsonify({"message": "An unexpected error occurred", "error": str(e)}),
                500,
            )


class SingleProduct(Resource):
    def get(self, product_id):
        try:
            product = Product.query.get(product_id)
            if not product:
                return make_response(jsonify({"message": "Product not found"}), 404)
            return make_response(jsonify(product.to_dict()), 200)
        except SQLAlchemyError as e:
            return make_response(
                jsonify({"message": "Error fetching product", "error": str(e)}), 500
            )

    @jwt_required()
    @allow("admin")
    def patch(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return make_response(jsonify({"message": "Product not found"}), 404)

        data = request.get_json()
        print(data)
        try:
            for attr in data:
                setattr(product, attr, data[attr])
            db.session.commit()
            return make_response(jsonify(product.to_dict()), 200)
        except KeyError as e:
            db.session.rollback()
            return make_response(
                jsonify({"message": f"Missing required field: {str(e)}"}), 400
            )
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(
                jsonify({"message": "Database error occurred", "error": str(e)}), 500
            )
        except Exception as e:
            db.session.rollback()
            return make_response(
                jsonify({"message": "An unexpected error occurred", "error": str(e)}),
                500,
            )

    @jwt_required()
    @allow("admin")
    def delete(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return make_response(jsonify({"message": "Product not found"}), 404)

        try:
            db.session.delete(product)
            db.session.commit()
            return make_response(
                jsonify({"message": "Product deleted successfully"}), 200
            )
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(
                jsonify(
                    {
                        "message": "Database error occurred during deletion",
                        "error": str(e),
                    }
                ),
                500,
            )
        except Exception as e:
            db.session.rollback()
            return make_response(
                jsonify(
                    {
                        "message": "An unexpected error occurred during deletion",
                        "error": str(e),
                    }
                ),
                500,
            )


api.add_resource(Products, "/products", endpoint="products")
api.add_resource(SingleProduct, "/products/<int:product_id>", endpoint="single_product")
