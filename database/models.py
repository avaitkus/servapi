from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from mongoengine import *

class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    name = db.StringField(required=True, unique=True)
    group = db.StringField(required=True, unique=False)
#    prefix = StringField(required=True, unique=False)
    store_prices_path = db.StringField(required=True, unique=False)
    products_path = db.StringField(required=True, unique=False)
    metadatas = db.ListField(required=True, unique=False)
    
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    

