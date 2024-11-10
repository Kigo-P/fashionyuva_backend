from models import Review
from flask import Blueprint, make_response, jsonify
from flask_restful import Api, Resource

review = Blueprint("review", __name__)
api = Api(review)