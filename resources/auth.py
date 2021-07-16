import logging
from flask import request, make_response, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource
import datetime
from database.models import User
#from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.errors import UnauthorizedError, InvalidPasswordError


class SignupApi(Resource):
    @jwt_required()
    def post(self):
        token = get_jwt_identity()
        if 'Administrator@omvi.lt' == str(token.split("_")[2]):
            name = str(token.split("_")[1])
            body = request.get_json()
            user =  User(**body)
            user.hash_password()
            user.save()
            id = user.id
            result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": name, "HTTP_method": "POST SignUp", "new_user": user.name})
            logging.info(str(datetime.today()) + ' ' + request.remote_addr + ' ' + name+ " POST Signup new_user: " + user.name)
            return make_response(jsonify(user), 200)
        else:
            raise UnauthorizedError

class UserDataUpdateApi(Resource):
    @jwt_required()
    def post(self):
        token = get_jwt_identity()
        if 'Administrator@omvi.lt' == str(token.split("_")[2]):
            name = str(token.split("_")[1])
            body = request.get_json()
            user = User.objects.get(name=body.get('name'))
            user.store_prices_path =  body.get('store_prices_path')
            user.products_path =  body.get('products_path')
            user.metadatas = body.get('metadatas')
            user.update(products_path=user.products_path, store_prices_path=user.store_prices_path, metadatas=user.metadatas)
            result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": name, "HTTP_method": "POST UserDateUpdate",  "user_updated": user.name})
            logging.info(str(datetime.today()) + ' ' + request.remote_addr +' ' + name+" POST UserDateUpdate user "+user.name+" updated")
            return make_response(jsonify(user), 200)
        else:
            raise UnauthorizedError

class UsersApi(Resource):
    @jwt_required()
    def get(self):    
        token = get_jwt_identity()
        if 'Administrator@omvi.lt' == str(token.split("_")[2]):
            name = str(token.split("_")[1])
            username = request.args.get('name', default = "all", type = str)
            group = request.args.get('group', default = "all", type = str)            
            if name != "all":
                user = User.objects.get(name=username)
            elif group != "all":
                user = User.objects.filter(group=group)
            else:            
                user = User.objects.filter()
            result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": name, "HTTP_method": "Get Users"})
            logging.info(str(datetime.today()) + ' ' + request.remote_addr +' ' +name+" GET Users")
            return make_response(jsonify(user), 200)
        else:
            raise UnauthorizedError
    

            
class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        if 'password' == body.get('password'):
            raise InvalidPasswordError
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            raise UnauthorizedError
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity="future_" + str(user.name) + "_" + str(user.group), expires_delta=expires)
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": user.name, "HTTP_method": "POST Login"})
        logging.info(str(datetime.today()) + ' ' + request.remote_addr +' ' +user.name+" POST Login")
        return make_response(jsonify({'token': access_token}), 200)
        
class ChangePassApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            raise UnauthorizedError
        user.password =  body.get('new_password')
        user.hash_password()
        user.update(password=user.password)
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": user.name, "HTTP_method": "POST ChangePass"})
        logging.info(str(datetime.today()) + ' ' + request.remote_addr +' ' +user.name+" POST ChangePass")
        return make_response(jsonify({'user': user.name}), 200)
            
    
