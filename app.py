from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from config import Config
from models import db
from products import products
from users import users
from contacts import contactus
from address import address
from reviews import review
from orders import orders
from order_product import order_product
from payment import payment


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

app.register_blueprint(products)
app.register_blueprint(users)
app.register_blueprint(contactus)
app.register_blueprint(address)
app.register_blueprint(review)
app.register_blueprint(orders)
app.register_blueprint(order_product)
app.register_blueprint(payment)


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


    # for mpesa 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    from app.routes.payment import payment_bp
    app.register_blueprint(payment_bp, url_prefix='/api/payment')
    
    with app.app_context():
        db.create_all()
    
    return app
