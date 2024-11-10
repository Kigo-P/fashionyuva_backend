from models import Payment
from flask import Blueprint, make_response, jsonify
from flask_restful import Api, Resource

payment = Blueprint("payment", __name__)
api = Api(payment)