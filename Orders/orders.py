from models import Order, db
from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource
from authentification.auth import allow
from flask_jwt_extended import jwt_required

orders = Blueprint("orders", __name__)
api = Api(orders)

class Orders(Resource):
    @jwt_required()
    @allow("admin")
    def get(self):
        orders = Order.query.all()
        order_dict = [order.to_dict() for order in orders]
        response = make_response(order_dict, 200)
        return response

    @jwt_required()
    @allow("customer")
    def post(self):
        data = request.get_json()
        new_order = Order(
            total_price = data["total_price"],
            status = data["status"],
            user_id = data["user_id"],
        )

        db.session.add(new_order)
        db.session.commit()

        new_order_dict = new_order.to_dict()
        response = make_response(new_order_dict, 201)
        return response
    pass

class OrdersById(Resource):
    @jwt_required()
    @allow("customer", "admin")
    def get(self, id):
        order = Order.query.filter_by(id=id).first()
        if order:
            order_dict = order.to_dict()
            response = make_response(order_dict, 200)
            return response
        else:
            response_body = {"message":"Order not found :("}
            response = make_response(response_body, 404)
            return response


    def patch(self, id):
        order = Order.query.filter_by(id=id).first()
        if order:
            data = request.get_json()
            for attr in data:
                setattr(order, attr, data[attr])

                db.session.commit()

                order_dict = order.to_dict()
                response = make_response(order_dict, 200)
                return response
            else:
                response_body = {"message":"Order not found :("}
                response = make_response(response_body, 404)
                return response

    def delete(self, id):
        order = Order.query.filter_by(id=id).first()
        if order:
            db.session.delete(order)
            db.session.commit()

            response_body = {"message":"Order deleted successfully:)"}
            response = make_response(response_body, 204)
            return response
        else:
            response_body = {"error": "Order not found:("}
            response = make_response(response_body, 404)
            return response

    pass

api.add_resource(Orders, "/orders", endpoint="order")
api.add_resource(OrdersById, "/orders/<int:id>",endpoint = "orders_by_id")


        

    