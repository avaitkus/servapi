import pymongo, logging
from flask import request, json, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from datetime import datetime, timedelta
from decouple import config
from woocommerce import API
from database.db import mydb, log_remote_col
from resources.errors import UnauthorizedError, InvalidFileNameError
from database.models import User

consumer_key = config('CONSUMER_KEY')
consumer_secret = config('CONSUMER_SECRET')
logging_file = config('LOGGING_FILE')
logging.basicConfig(filename=logging_file, level=logging.INFO)
products_schema_ext = json.loads(config('PRODUCTS_SCHEMA_EXT'))
products_schema = json.loads(config('PRODUCTS_SCHEMA'))
data_path = config('DATA_PATH')

class StorePricesApi(Resource):
    @jwt_required()
    def get(self):
        token = get_jwt_identity()
        name = str(token.split("_")[1])
        group = str(token.split("_")[2])
        user = User.objects.get(name=name)
        language = request.args.get('language', default = "lt", type = str)
        page = request.args.get('page', default = 1, type = int)
        per_page = request.args.get('per_page', default = 20, type = int)
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": user.name, "HTTP_method": "GET StorePrices", "page": page, "per_page": per_page})
        logging.info(str(datetime.today()) +" "+ request.remote_addr +" "+ user.name+" GET StorePrice")
        if user.store_prices_path == "db":
            col = mydb["products"]
            cursor = col.find({},{"_id": 0,"sku": 1, "stock_quantity":1, "meta_data": 1}).sort("_id").skip((page-1)*per_page).limit(per_page)
            products =list(cursor)
            metadatas = user.metadatas
            for product in products:
                for metadata in product["meta_data"]:
                    if metadata["key"] in metadatas:
                        product[metadata["key"]]=metadata["value"]
                del product["meta_data"]
            response = make_response(jsonify(products), 200)
            response.headers["X-Total"] = str(cursor.count())
            response.headers["X-Total-Pages"] = str(int((int(cursor.count())-1)/per_page)+1)
            logging.info(str(response.headers["X-Total"]))
            return response
        elif user.store_prices_path == "suspended":
            raise UnauthorizedError
        else:
            try:
                with open(user.store_prices_path + ".json") as f:
                    data = json.load(f)
            except:
                raise InvalidFileNameError
            return make_response(jsonify(data), 200)

class ProductsApi(Resource): 
    @jwt_required()
    def get(self):
        token = get_jwt_identity()
        file_name = ""
        name = str(token.split("_")[1])
        group = str(token.split("_")[2])
        user = User.objects.get(name=name)
        language = request.args.get('language', default = "lt", type = str)
        page = request.args.get('page', default = 1, type = int)
        per_page = request.args.get('per_page', default = 20, type = int)
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": user.name, "HTTP_method": "GET Products", "page": page, "per_page": per_page, "language": language})
        logging.info(str(datetime.today())+' ' + request.remote_addr +' ' +user.name+" GET Products"+'_'+language)
        if user.products_path == "suspended":
            raise UnauthorizedError
        elif user.products_path == "db":
            if language =="all":
                col = mydb["products"]
                projection = products_schema
                properties = config("LANGUAGE_SPECIFIC_PROPERTIES").split(",")
                languages =config("LANGUAGES").split(",")
                for prop in properties:
                    for lang in languages:
                        projection[prop+"_"+lang]=1
            else:
                col = mydb["products"+"_"+language]
                projection = products_schema_ext
            cursor = col.find({},projection).sort("_id").skip((page-1)*per_page).limit(per_page)
            products =list(cursor)

            response = make_response(jsonify(products), 200)
            response.headers["X-Total"] = str(cursor.count())
            response.headers["X-Total-Pages"] = str(int((int(cursor.count())-1)/per_page)+1)

            logging.info("served from db "+ str(cursor.count()))
            return response
        else:
            try:
                with open(user.products_path+"_"+language+ ".json") as f:
                    data = json.load(f)
                logging.info("served from " + user.products_path + "_" + language+ ".json "+  str(len(data))+ " products")
                return make_response(jsonify(data), 200)
            except:
                raise InvalidFileNameError

class OmviStoreToOmviProductsApi(Resource):
    @jwt_required()
    def get(self):
        token = get_jwt_identity()
        if 'Administrator@omvi.lt' == str(token.split("_")[2]):
            name = str(token.split("_")[1])
            page = request.args.get('page', default = 1, type = int)
            per_page= request.args.get('per_page', default = 20, type = int)
            language = request.args.get('language', default = "lt", type = str)
            languages = config("LANGUAGES").split(",")
            logging.info(str(datetime.today()) +" "+ request.remote_addr +" "+ name+" GET OmviStoreToOmviProducts")
            result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": name, "HTTP_method": "GET OmviStoreToOmviProducts", "language": language})
            report ={}
            if language =="all":
                col = mydb["products"]
            else:
                col = mydb["products"+"_"+language]
                languages = [language]
            for lang in languages:
                updates = 0
                page = 1
                api_parameter = "products?status=publish&per_page=" + str(per_page) + "&page=" + str(page) + "&lang=" + lang
                url = "https://omvi.store"
                wcapi = API(url=url, consumer_key=consumer_key, consumer_secret=consumer_secret, version="wc/v3")
                next="next"
                while "next" in next:
                    while True:
                        logging.info(api_parameter)
                        try:
                            dat = wcapi.get(api_parameter)#.json()
                            break
                        except:
                            continue
                    header = dat.headers
                    datas = dat.json()
                    next = header['Link']
                    if 'next' in header['Link']:
                        page += 1
                        api_parameter= "products?status=publish&per_page=" + str(per_page) + "&page=" + str(page) + "&lang=" + lang
                    else:
                        next = ''
                    for product in datas:
                        if language == "all":
                            properties = config("LANGUAGE_SPECIFIC_PROPERTIES").split(",")
                            for prop in properties:
                                product[prop+"_"+product["lang"]]=product[prop]
#                        result= col.update_one({'sku':product['sku']}, {'$set':product}, upsert=True)
                        updates += 1
                report[lang] = str(updates) +" " + lang + " records updated in colection " + col.name
            logging.info("db sinchronized with omvi.store")
            return make_response(jsonify(report), 200)
        else:
            raise UnauthorizedError
            
class LogRemoteApi(Resource):
    @jwt_required()
    def get(self):
        token = get_jwt_identity()
        if 'Administrator@omvi.lt' == str(token.split("_")[2]):
            name = str(token.split("_")[1])
            history_days = request.args.get('history_days', default = 7, type = int)
            diena = datetime.today()
            delta = timedelta(days=history_days)
            IP_remote = request.args.get('IP', default = "all", type = str)
            user = request.args.get('user', default = "all", type =str)
            query ={"date":{'$gte':diena-delta, "$lt":diena}}
            if IP_remote != "all":
                query["IP_remote"]=IP_remote
            if user != "all":
                query["user"]=user
            logging.info(str(datetime.today()) +" "+ request.remote_addr +" "+ name+" GET LogRemote "+ str(query))
            cursor = log_remote_col.find(query, {"_id": 0, "date":1, "IP_remote":1, "user":1, "HTTP_method":1})
            history = list(cursor)
            result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": name, "HTTP_method": "GET LogRemote", "query": query})
            return make_response(jsonify(history), 200)
        else:
            raise UnauthorizedError
            
class LogRemoteDeleteApi(Resource):
    @jwt_required()
    def get(self):
        token = get_jwt_identity()
        if 'Administrator@omvi.lt' == str(token.split("_")[2]):
            name = str(token.split("_")[1])
            keep_history_days = request.args.get('keep_history_days', default = 7, type = int)
            diena = datetime.today()
            delta = timedelta(days=keep_history_days)
            IP_remote = request.args.get('IP', default = "all", type = str)
            user = request.args.get('user', default = "all", type =str)
            query ={"date":{'$lt':diena-delta}}
            if IP_remote != "all":
                query["IP_remote"]=IP_remote
            if user != "all":
                query["user"]=user
            before = log_remote_col.find().count()
            cursor = log_remote_col.delete_many(query)
            after = log_remote_col.find().count()
            logging.info(str(datetime.today()) +" "+ request.remote_addr +" "+ name+" GET LogRemoteDelete "+ str(query)+ str(before)+ "-->"+str(after))
            result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": name, "HTTP_method": "GET LogRemoteDelete", "query": query, "records_before": before, "records_after": after})
            return "deleted: IP_remote: "+ str(before-after)+' records '+str(query), 200
        else:
            raise UnauthorizedError


class LoggingFileDeleteApi(Resource):
    @jwt_required()
    def post(self):
        token = get_jwt_identity()
        if 'Administrator@omvi.lt' ==str(token.split("_")[2]):
            name = str(token.split("_")[1])
            with open(logging_file,'w') as f:
                f.write("")
            logging.info(str(datetime.today()) +" "+ request.remote_addr +" "+ name+" GET LoggingFileDelete")
            result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": name, "HTTP_method": "GET LoggingFileDelete", "logging_file": logging_file})
            return logging_file + " is cleared",200
        else:
            raise UnauthorizedError
                
        
