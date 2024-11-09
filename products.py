from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource
from models import Product, db

products = Blueprint("products", __name__)
api = Api(products)


class Products(Resource):
    def get(self):
        products = Product.query.all()
        return make_response(jsonify([product.to_dict() for product in products]), 200)

    def post(self):
        data = request.get_json()
        try:
            new_product = Product(
                title=data["title"],
                description=data["description"],
                price=data["price"],
                size=data["size"],
                color=data["color"],
                material=data["material"],
                quantity=data["quantity"],
                image_id=data.get("image_id"),
                category_id=data.get("category_id"),
            )
            db.session.add(new_product)
            db.session.commit()
            return make_response(jsonify(new_product.to_dict()), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 400)


class SingleProduct(Resource):
    def get(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return make_response(jsonify({"error": "Product not found"}), 404)
        return make_response(jsonify(product.to_dict()), 200)

    def put(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return make_response(jsonify({"error": "Product not found"}), 404)

        data = request.get_json()
        try:
            product.title = data.get("title", product.title)
            product.description = data.get("description", product.description)
            product.price = data.get("price", product.price)
            product.size = data.get("size", product.size)
            product.color = data.get("color", product.color)
            product.material = data.get("material", product.material)
            product.quantity = data.get("quantity", product.quantity)
            product.image_id = data.get("image_id", product.image_id)
            product.category_id = data.get("category_id", product.category_id)

            db.session.commit()
            return make_response(jsonify(product.to_dict()), 200)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 400)

    def delete(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return make_response(jsonify({"error": "Product not found"}), 404)

        try:
            db.session.delete(product)
            db.session.commit()
            return make_response(
                jsonify({"message": "Product deleted successfully"}), 200
            )
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 400)


api.add_resource(Products, "/products", endpoint="products")
api.add_resource(SingleProduct, "/products/<int:product_id>", endpoint="single_product")
