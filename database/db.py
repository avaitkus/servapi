import pymongo
from flask_mongoengine import MongoEngine
db = MongoEngine()

client =pymongo.MongoClient("mongodb://localhost:27017/", username='servapi',password ='Santana*713', authSource = 'admin')
mydb = client["servapi"]

log_remote_col = mydb["log_remote"]

def initialize_db(app):
    db.init_app(app)
