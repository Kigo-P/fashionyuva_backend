from models import ContactUs, db
from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource


contact_us = Blueprint("contact_us", __name__)
api = Api(contact_us)


class ContactUss(Resource):
    def get(self):
        contacts = ContactUs.query.all()
        contact_dict = [contact.to_dict() for contact in contacts]
        response = make_response(contact_dict, 200)
        return response

    def post(self):
        data = request.get_json()
        new_contact = ContactUs(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            contact=data["contact"],
            message=data["message"],
        )
        db.session.add(new_contact)
        db.session.commit()
        new_contact_dict = new_contact.to_dict()
        response = make_response(new_contact_dict, 201)
        return response


class ContactUsById(Resource):
    def get(self, id):
        contact = ContactUs.query.filter_by(id=id).first()
        if contact:
            contact_dict = contact.to_dict()
            response = make_response(contact_dict, 200)
            return response
        else:
            response_body = {"error": "Contact not found"}
            response = make_response(response_body, 404)
            return response

    def patch(self, id):
        contact = ContactUs.query.filter_by(id=id).first()
        if contact:
            data = request.get_json()
            for attr in data:
                setattr(contact, attr, data[attr])
            db.session.commit()
            contact_dict = contact.to_dict()
            response = make_response(contact_dict, 200)
            return response
        else:
            response_body = {"message": "Contact not found"}
            response = make_response(response_body, 404)
            return response

    def delete(self, id):
        contact = ContactUs.query.filter_by(id=id).first()
        if contact:
            db.session.delete(contact)
            db.session.commit()
            response_body = {"message": "Contact deleted successfully"}
            response = make_response(response_body, 204)
            return response
        else:
            response_body = {"error": "Contact not found"}
            response = make_response(response_body, 404)
            return response


api.add_resource(ContactUss, "/contacts", endpoint="contacts")
api.add_resource(ContactUsById, "/contacts/<int:id>", endpoint="contacts_by_id")