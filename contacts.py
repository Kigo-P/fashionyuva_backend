from models import ContactUs
from flask import Blueprint, make_response, jsonify
from flask_restful import Api, Resource

contactus = Blueprint("contactus", __name__)
api = Api(contactus)