from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from config import Config


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

api = Api(app)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
