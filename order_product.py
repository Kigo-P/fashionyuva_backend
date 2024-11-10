from models import OrderProduct
from flask import Blueprint, make_response, jsonify
from flask_restful import Api, Resource

order_product = Blueprint("order_product", __name__)
api = Api(order_product)