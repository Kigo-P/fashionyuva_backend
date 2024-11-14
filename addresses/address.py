from models import Address, db
from flask import Blueprint, make_response, jsonify, request  
from flask_restful import Api, Resource

address = Blueprint("address", __name__)
api = Api(address)

class AddressResource(Resource):
    
    def get(self):
        addresses = Address.query.all()
        addresses_list = [address.to_dict(rules=("-user",)) for address in addresses]
        return make_response(jsonify({"addresses": addresses_list}), 200)

    def post(self):
        data = request.get_json()
        
        required_fields = ["address", "county", "town", "zip_code", "country"]
        if not all(field in data for field in required_fields):
            return make_response(jsonify({"error": "Missing required fields"}), 400)

        new_address = Address(
            user_id=data.get("user_id"),
            address=data["address"],
            county=data["county"],
            town=data["town"],
            zip_code=data["zip_code"],
            country=data["country"]
        )
        
        try:
            db.session.add(new_address)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)
        
        return make_response(jsonify(new_address.to_dict()), 201)

class SingleAddressResource(Resource):
    
    def get(self, address_id): 
        address = Address.query.get(address_id)
        if not address:
            return make_response(jsonify({"error": "Address not found"}), 404)
        
        return make_response(jsonify(address.to_dict(rules=("-user",))), 200)

    def patch(self, address_id):
        address = Address.query.get(address_id)
        if not address:
            return make_response(jsonify({"error": "Address not found"}), 404)
        
        data = request.get_json()
        
        for field in ["address", "county", "town", "zip_code", "country"]:
            if field in data:
                setattr(address, field, data[field])
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)
        
        return make_response(jsonify(address.to_dict()), 200)

    def delete(self, address_id):
        address = Address.query.get(address_id)
        if not address:
            return make_response(jsonify({"error": "Address not found"}), 404)
        
        try:
            db.session.delete(address)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 500)
        
        return make_response(jsonify({"message": "Address deleted successfully"}), 204)

api.add_resource(AddressResource, "/addresses", endpoint="addresses")
api.add_resource(SingleAddressResource, "/addresses/<int:address_id>", endpoint="address")
