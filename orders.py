from models import Order
from flask import Blueprint, make_response, jsonify
from flask_restful import Api, Resource

orders = Blueprint("orders", __name__)
api = Api(orders)