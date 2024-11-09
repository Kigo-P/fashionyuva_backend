from models import Address
from flask import Blueprint, make_response, jsonify
from flask_restful import Api, Resource

address = Blueprint("address", __name__)
api = Api(address)