from flask_jwt_extended import create_access_token,get_jwt,JWTManager,create_refresh_token,jwt_required,get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource, Api, reqparse
from flask import Blueprint, jsonify, make_response, request
import datetime
from datetime import timezone
from functools import wraps
from models import User, TokenBlocklist, db




jwt = JWTManager()

auth = Blueprint("auth", _name_, url_prefix="/auth")
api = Api(auth)


from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

#  creating a custom hook that helps in knowing the roles of either the buyer or the administrator
# a method called allow that uses the user roles and give users certain rights to access certain endpoints
def allow(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):  
            jwt_claims=get_jwt()
            user_role=jwt_claims.get('role',None)
            
            # Check if the user_role is in the allowed roles
            if user_role in roles:
                return fn(*args, **kwargs)
            else:
                # creating and returning a response based on the response_body
                response_body = {"message": "Access is forbidden"}
                response = make_response(response_body, 403)
                return response

        return decorator

    return wrapper

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

# confirming whether the jti is in the token blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_blocklist = TokenBlocklist.query.filter_by(jti=jti).first()
    return token_in_blocklist or None

# creating a Login resource
class Login(Resource):
    def post(self):
        # checking the user email
        data = request.get_json()
        email = data["email"]
        # querying the users email while logging in
        user = User.query.filter_by(email = email).first()
        #  if the user does not exist then return a message
        if not user:
            #  creating and returning a response based on the response body
            response_body = {"message": f"User with email {email} does not exist"}
            response = make_response(response_body, 404)
            return response
        
        #  checking whether the passwords are similar(the one in the database vs the one given by user), if not then throw an error
        if not check_password_hash(user.password, data["password"]):
            #  creating and returning a response based on the response body
            response_body = {"message": "The password entered is incorrect"}
            response = make_response(response_body, 403)
            return response

        #  creating an access token and a refresh token
        access_token = create_access_token(identity=user.id, additional_claims={"role":user.user_role})
        refresh_token = create_refresh_token(identity=user.id)
        # converting user to a dictionary
        user1 = user.to_dict()
        return{
            "message": "Logged in",
            "user_data": user1,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role":user.user_role
        }
    
    #  a method to refresh the token
    @jwt_required(refresh = True)
    def get(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        response = jsonify(access_token=access_token)
        return response

    pass

# creating a Logout Resource
class Logout(Resource):
    # creating a get method 
    @jwt_required()
    def get(self):
        jti = get_jwt()["jti"]
        # using the date time to track the date and time the user has logged out
        now = datetime.datetime.now(timezone.utc)
        # adding and commiting the TokenBlocklist 
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        # creating and returning a response
        response = {"message": "You have been logged out"}
        return response

api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="login")