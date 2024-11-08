from flask import Blueprint, make_response, jsonify
from flask_restful import Api, Resource
from models import Product

products = Blueprint("products", __name__)
api = Api(products)


class Products(Resource):

    def get(self):
        products = Product.query.all()
        return make_response(jsonify([product.to_dict() for product in products]), 200)


api.add_resource(Products, "/products", endpoint="products")
