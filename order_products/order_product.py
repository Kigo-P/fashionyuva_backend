from models import OrderProduct, db
from flask import Blueprint, make_response, jsonify, request
from flask_restful import Api, Resource

order_product = Blueprint("order_product", __name__)
api = Api(order_product)


class OrderProducts(Resource):
    #  a method to get all order_products
    def get(self):
        # querying the database to get a list of all the order_products
        orderProducts = OrderProduct.query.all()
        # Looping through order_products and getting a user as a dictionary using to_dict() method
        orderproduct_dict = [orderproduct.to_dict() for orderproduct in orderProducts]
        # creating and making a response
        response = make_response(orderproduct_dict, 200)
        return response

    # a method to post an order_product

    def post(self):
        data = request.get_json()
        new_orderproducts = []

        for prod in data["cart"]:
            new_orderproduct = OrderProduct(
                quantity=prod["quantity"],
                product_id=prod["id"],
                order_id=prod.get("order_id", prod["order_id"]),
            )
            db.session.add(new_orderproduct)
            db.session.flush()
            new_orderproducts.append(new_orderproduct.to_dict())

        db.session.commit()
        response = make_response(jsonify(new_orderproducts), 201)
        return response


# creating a OrderProductsById Resource
class OrderProductsById(Resource):
    #  a method to get one orderproduct
    def get(self, id):
        # querying and filtering the database using the id
        orderproduct = OrderProduct.query.filter_by(id=id).first()
        if orderproduct:
            #  creating a orderproduct dict using the to_dict method
            orderproduct_dict = orderproduct.to_dict()
            # creating and making a response
            response = make_response(orderproduct_dict, 200)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"message": "OrderProduct not found"}
            response = make_response(response_body, 404)
            return response

    #  a method to update an orderproduct
    def patch(self, id):
        # querying and filtering the database using the id
        orderproduct = OrderProduct.query.filter_by(id=id).first()
        if orderproduct:
            data = request.get_json()
            #  creating a for loop to set the attributes
            for attr in data:
                setattr(orderproduct, attr, data[attr])

            # commiting to the database
            db.session.commit()
            #  making orderproduct to a dictionary
            orderproduct_dict = orderproduct.to_dict()
            response = make_response(orderproduct_dict, 200)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"message": "OrderProduct not found"}
            response = make_response(response_body, 404)
            return response

    #  a method to delete the review
    def delete(self, id):
        orderproduct = OrderProduct.query.filter_by(id=id).first()
        if orderproduct:
            db.session.delete(orderproduct)
            db.session.commit()

            #  creating and returning a response based on the response body
            response_body = {"message": "OrderProduct deleted successfully"}
            response = make_response(response_body, 204)
            return response
        else:
            #  creating and returning a response based on the response body
            response_body = {"error": "OrderProduct not found"}
            response = make_response(response_body, 404)
            return response

    pass


api.add_resource(OrderProducts, "/order-products", endpoint="order_products")
api.add_resource(
    OrderProductsById, "/order-products/<int:id>", endpoint="order_products_by_id"
)
