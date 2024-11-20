from datetime import timezone, datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from config import Config
from models import TokenBlocklist, User, db
from products.products import products
from users.users import users
from contact.contacts import contact_us
from addresses.address import address
from reviews.reviews import review
from Orders.orders import orders
from authentification.auth import auth
from order_products.order_product import order_product
from flask_jwt_extended import JWTManager
from payment.mpesa import payment
from newsletters.newsletter import newsletter
from categories.category import category
from analytics.analytics import analytics


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(products)
app.register_blueprint(users)
app.register_blueprint(contact_us)
app.register_blueprint(address)
app.register_blueprint(review)
app.register_blueprint(orders)
app.register_blueprint(order_product)
app.register_blueprint(payment, url_prefix="/api/payment")
app.register_blueprint(newsletter)
app.register_blueprint(category)
app.register_blueprint(analytics)


db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

with app.app_context():
    db.create_all()


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "message": "The token has expired. Please log in again.",
                "error": "token_expired",
            }
        ),
        401,
    )


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()


# confirming whether the jti is in the token blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    now = datetime.now(timezone.utc)
    expiration = datetime.fromtimestamp(jwt_payload["exp"], timezone.utc)

    if now > expiration:
        return True
    return TokenBlocklist.query.filter_by(jti=jti).first() is not None


@app.before_request
def handle_options_request():
    if request.method == "OPTIONS":
        response = make_response("", 200)
        response.headers["Allow"] = ("GET, POST, PUT, DELETE, OPTIONS", "PATCH")
        return response


class Wake(Resource):
    def get(self):
        return make_response(jsonify({"message": "server is awake"}), 200)


api.add_resource(Wake, "/wake", endpoint="wake")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
