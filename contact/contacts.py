from models import ContactUs, db
from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError

contact_us = Blueprint("contact_us", __name__)
api = Api(contact_us)


class ContactUss(Resource):
    def get(self):
        try:
            contacts = ContactUs.query.all()
            contact_dict = [contact.to_dict() for contact in contacts]
            response = make_response(contact_dict, 200)
            return response
        except SQLAlchemyError as e:
            response_body = {"message": "Failed to fetch contacts", "error": str(e)}
            return make_response(response_body, 500)

    def post(self):
        try:
            data = request.get_json()
            new_contact = ContactUs(
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                contact=data["contact"],
                message=data["message"],
                about_us=data["about_us"],
            )
            db.session.add(new_contact)
            db.session.commit()
            new_contact_dict = new_contact.to_dict()
            response = make_response(new_contact_dict, 201)
            return response
        except KeyError as e:
            response_body = {"message": f"Missing required field: {str(e)}"}
            return make_response(response_body, 400)
        except SQLAlchemyError as e:
            response_body = {"message": "Failed to create contact", "error": str(e)}
            return make_response(response_body, 500)


class ContactUsById(Resource):
    def get(self, id):
        try:
            contact = ContactUs.query.filter_by(id=id).first()
            if contact:
                contact_dict = contact.to_dict()
                response = make_response(contact_dict, 200)
                return response
            else:
                response_body = {"message": "Contact not found"}
                return make_response(response_body, 404)
        except SQLAlchemyError as e:
            response_body = {"message": "Failed to fetch contact", "error": str(e)}
            return make_response(response_body, 500)

    def patch(self, id):
        try:
            contact = ContactUs.query.filter_by(id=id).first()
            if contact:
                data = request.get_json()
                for attr in data:
                    if hasattr(contact, attr):
                        setattr(contact, attr, data[attr])
                db.session.commit()
                contact_dict = contact.to_dict()
                response = make_response(contact_dict, 200)
                return response
            else:
                response_body = {"message": "Contact not found"}
                return make_response(response_body, 404)
        except SQLAlchemyError as e:
            response_body = {"message": "Failed to update contact", "error": str(e)}
            return make_response(response_body, 500)

    def delete(self, id):
        try:
            contact = ContactUs.query.filter_by(id=id).first()
            if contact:
                db.session.delete(contact)
                db.session.commit()
                response_body = {"message": "Contact deleted successfully"}
                response = make_response(response_body, 204)
                return response
            else:
                response_body = {"message": "Contact not found"}
                return make_response(response_body, 404)
        except SQLAlchemyError as e:
            response_body = {"message": "Failed to delete contact", "error": str(e)}
            return make_response(response_body, 500)


api.add_resource(ContactUss, "/contacts", endpoint="contacts")
api.add_resource(ContactUsById, "/contacts/<int:id>", endpoint="contacts_by_id")
