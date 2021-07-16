import logging
from decouple import config
from time import localtime, strftime
from datetime import datetime
from woocommerce import API
from flask import Flask, json,jsonify, make_response, request
from waitress import serve
from flask_restful import Resource
#app = Flask(__name__)

consumer_key = config('CONSUMER_KEY')
consumer_secret = config('CONSUMER_SECRET')

logging_file = config('LOGGING_FILE')
logging.basicConfig(filename=logging_file, level=logging.INFO)
logging.info(str(datetime.today()) +' servapi started')
servapi_path = config('SERVAPI_DATA_PATH')

#    open access backend
#    returns product descriptions in xx language from PricelistA_xx.json, servapi_path directory as 

class GetProductsLTApi(Resource):
    def get(self):
        logging.info(str(datetime.today())+' ' + request.remote_addr +' ' + 'user N/A servapi@GET: PricelistA_lt.json')
        with open(servapi_path+"PricelistA_lt.json") as f:
            data = json.load(f)
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "HTTP_method": "GET GetProductsLT"})
        logging.info(str(datetime.today()) + ' served')
        return make_response(jsonify(data), 200)

class GetProductsLVApi(Resource):
    def get(self):
        logging.info(str(datetime.today())+' ' + request.remote_addr +' ' + 'user N/A servapi@GET: PricelistA_lv.json')
        with open(servapi_path+"PricelistA_lv.json") as f:
            data = json.load(f)
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "HTTP_method": "GET GetProductsLV"})
        logging.info(str(datetime.today()) + ' served')
        return make_response(jsonify(data), 200)

class GetProductsETApi(Resource):
    def get(self):
        logging.info(str(datetime.today())+' ' + request.remote_addr +' ' + 'user N/A servapi@GET: PricelistA_et.json')
        with open(servapi_path+"PricelistA_et.json") as f:
            data = json.load(f)
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "HTTP_method": "GET GetProductsET"})
        logging.info(str(datetime.today()) + ' served')
        return make_response(jsonify(data), 200)

class GetProductsENApi(Resource):
    def get(self):
        logging.info(str(datetime.today())+' ' + request.remote_addr +' ' + 'user N/A servapi@GET: PricelistA_en.json')
        with open(servapi_path+"PricelistA_en.json") as f:
            data = json.load(f)
        logging.info(str(datetime.today()) + ' served')
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "HTTP_method": "GET GetProductsEN"})
        return make_response(jsonify(data), 200)

class GetProductsRUApi(Resource):
    def get(self):
        logging.info(str(datetime.today())+' ' + request.remote_addr +' ' + 'user N/A servapi@GET: PricelistA_ru.json')
        with open(servapi_path+"PricelistA_ru.json") as f:
            data = json.load(f)
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "HTTP_method": "GET GetProductsRU"})
        logging.info(str(datetime.today()) + ' served')
        return make_response(jsonify(data), 200)


class GetPricelistaApi(Resource):
    def get(self):
        logging.info(str(datetime.today())+' ' + request.remote_addr +' ' + 'user N/A servapi@GET: PricelistA.json')
        with open(servapi_path+"PricelistA.json") as f:
            data = json.load(f)
        logging.info(str(datetime.today()) + ' served')
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": name, "HTTP_method": "GET GetProductsLT"})
        return make_response(jsonify(data), 200)

class GetVWholesaleApi(Resource):
    def get(self):
        logging.info(str(datetime.today())+' ' + request.remote_addr +' ' + 'user N/A servapi@GET: v_wholesale.json')
        with open(servapi_path+"v_wholesale.json") as f:
            data = json.load(f)
        logging.info(str(datetime.today()) + ' served')
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "user": name, "HTTP_method": "GET GetVWholesale"})
        return make_response(jsonify(data), 200)

class CreateDescriptionsApi(Resource):
    def get(self): #post for webhook needed
        langs = ["lv", "en", "et", "ru", "lt"]
        for lang in langs:
            logging.info(str(datetime.today())+' ' + request.remote_addr +' ' + 'user N/A servapi@Create: PricelistA_'+lang+'.json')
            data = []
            data_page = ["start"]
            page = 1
            per_page = 20
            url = "https://omvi.store"

            while data_page:
                data_page = []
                api_parameter = "products?status=publish&per_page=" + str(per_page) + "&page=" + str(page) + "&lang=" + lang
                #                print(api_parameter)
                wcapi = API(
                    url=url,
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    version="wc/v3"
                )
                try:
                    logging.info(str(datetime.today()) + ' ' + url +': '+ api_parameter)
                    data_page = wcapi.get(api_parameter).json()
                    page += 1
                except:
                    data_page = ["continue"]
                    logging.info(str(datetime.today()) + ' ' + url +': '+ api_parameter + ' retry')
                    continue
                if type(data_page) is list:
                    data = data + data_page
                if type(data_page) is dict:
                    data.append(data_page)

            tobe_kept = ["sku", "name", "description", "weight", "dimensions", "categories", "images", "attributes",
                    "translations", "lang", "id"]
            meta_kept = []

            if type(data) is list:
                logging.info(str(datetime.today())+' data type is list ')
                new_data = []
                new_dic = {}
                for product in data:
                    # new_dic = {k: product[k] for k in set(tobe_kept) & set(product.keys())}
                    new_dic = {}
                    for tobe in tobe_kept:
                        for key in product:
                            if tobe == key:
                                new_dic[key] = product[key]

                    meta_data_list = product["meta_data"]
                    for meta in meta_kept:
                        for meta_data in meta_data_list:
                            if meta_data["key"] == meta:
                                new_dic[meta] = meta_data["value"]
                    new_data.append(new_dic)
                data = new_data
            if type(data) is dict:
                logging.info(str(datetime.today())+' data type is dict ')
                new_dic = {k: data[k] for k in set(tobe_kept) & set(data.keys())}
                data = new_dic
            output_file = servapi_path+"PricelistA_" + lang + ".json"
            total = (len(data))
            with open(output_file, 'w', encoding='utf8') as json_file:
                json.dump(data, json_file, sort_keys=False, ensure_ascii=False, indent=4)
                logging.info(str(datetime.today())+ str(total)+'products saved to' + output_file)
        result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "HTTP_method": "GET CreateDescriptions"})
        return str(datetime.today()) +' '+ str(total)+ " products saved to PriselistA[_lt|_lv|_et|_et|_ru].json", 200

class CreateVPricelistApi(Resource):
    def get(self):
        logging.info(str(datetime.today())+' ' + request.remote_addr +' ' + 'user N/A servapi@Create: '+servapi_path+'v_wholesale.json')
        source = 'api'
        if source == 'api':
            data = []
            data_page = ["start"]
            page = 1
            per_page = 20
            lang = "lt"

            while data_page:
                data_page = []
                api_parameter = "products?status=publish&per_page=" + str(per_page) + "&page=" + str(page) + "&lang=" + lang
                url = "https://omvi.store"
                wcapi = API(
                    url=url,
                    consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    version="wc/v3"
                )
                try:
                    logging.info(str(datetime.today()) + ' ' + url +': '+api_parameter)
                    data_page = wcapi.get(api_parameter).json()
                    page += 1
                except:
                    data_page = ["continue"]
                    logging.info(str(datetime.today()) + ' ' + url +': '+api_parameter +' retry')
                    continue
                if type(data_page) is list:
                    data = data + data_page
                elif type(data_page) is dict:
                    data.append(data_page)
                else:
                    continue
        else:
            with open(source) as f:
                data = json.load(f)

        tobe_kept = config("TOBEKEPT").split(",")
        meta_kept = config("METAKEPT").split(",")
        if type(data) is list:
            logging.info(str(datetime.today())+' data type is list')
            new_data = []
            new_dic = {}
            for product in data:
                new_dic = {}
                for tobe in tobe_kept:
                    for key in product:
                        if tobe == key:
                            new_dic[key] = product[key]

                meta_data_list = product["meta_data"]
                for meta in meta_kept:
                     for meta_data in meta_data_list:
                        if meta_data["key"] == meta:
                            new_dic[meta] = meta_data["value"]
                new_data.append(new_dic)
            data = new_data
        if type(data) is dict:
            logging.info(str(datetime.today())+' data type is dict')
            new_dic = {k: data[k] for k in set(tobe_kept) & set(data.keys())}
            data = new_dic
        output_file = servapi_path+"v_wholesale.json"
        total = len(data)
        with open(output_file, 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, sort_keys=False, ensure_ascii=False, indent=4)
            logging.info(str(datetime.today())+ str(total)+'products updated in ' + output_file)
            result= log_remote_col.insert({"date": datetime.utcnow(), "IP_remote": request.remote_addr, "HTTP_method": "GET CreateVPricelist"})
        return str(datetime.today()) + str(total)+ " products are updated in " + output_file, 200

class TestApi(Resource):
    def get(self):
        logging.info(str(datetime.today())+' ' + request.remote_addr +' ' + 'user N/A servapi@5000 v1 veikia')
        return 'servapi@5000 v1 veikia', 200

