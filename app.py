from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from config import Config
from models import db
from products.products import products
from users.users import users
from contacts import contactus
from address import address
from reviews.reviews import review
from orders import orders
from authentification.auth import auth
from order_products.order_product import order_product
from payment.payment import payment
from flask_jwt_extended import JWTManager
from payment.mpesa import payment


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(products)
app.register_blueprint(users)
app.register_blueprint(contactus)
app.register_blueprint(address)
app.register_blueprint(review)
app.register_blueprint(orders)
app.register_blueprint(order_product)
# app.register_blueprint(payment)
app.register_blueprint(payment, url_prefix="/api/payment")


db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

with app.app_context():
    db.create_all()


class Wake(Resource):
    def get(self):
        return make_response(jsonify({"message": "server is awake"}), 200)


api.add_resource(Wake, "/wake", endpoint="wake")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
