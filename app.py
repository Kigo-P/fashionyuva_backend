from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from config import Config
from models import db
from products import products


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

app.register_blueprint(products)

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(port=5555, debug=True)
