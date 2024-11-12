from models import Newsletter
from flask import Blueprint, make_response, jsonify
from flask_restful import Api, Resource

newsletter = Blueprint("newsletter", __name__)
api = Api(newsletter)