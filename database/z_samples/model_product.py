from .db import db
from mongoengine import *

class MetaData(EmbeddedDocument):

    id = db.IntField
    key = db.StringField
    value = db.StringField


class Dimensions(EmbeddedDocument):
    length = db.StringField()
    width = db.StringField()
    height = db.StringField()
    
class Translations(EmbeddedDocument):
    en = db.StringField()
    et = db.StringField()
    lt = db.StringField()
    lv = db.StringField()
    ru = db.StringField()

class Category(EmbeddedDocument):
    id = db.IntField()
    name = db.StringField()
    slug = db.StringField()

class Image(EmbeddedDocument):
    id = db.IntField()
    date_created = db.DateTimeField()
    date_createdGmt = db.DateTimeField()
    date_modified = db.DateTimeField()
    date_modified_gmt = db.DateTimeField()
    src = db.StringField()
    name = db.StringField()
    alt = db.StringField()

class Attribute(EmbeddedDocument):
    id = db.IntField()
    name = db.StringField()
    position = db.IntField()
    visible = BooleanField()
    variation = BooleanField()
    options = db.ListField()

    
    

class Products(db.DynamicDocument):
    sku = db.StringField(required=True)
    name = db.StringField()
    description = db.StringField()
    weight = db.StringField()
    dimensions = db.DictField(EmbeddedDocumentField(Dimensions))
    categories = db.ListField(EmbeddedDocumentField(Category))
    images = db.ListField(EmbeddedDocumentField(Image))
    attributes = db.ListField(EmbeddedDocumentField(Attribute))
    translations = db.DictField(EmbeddedDocumentField(Translations))
    metadates = db.ListField(EmbeddedDocumentField(MetaData))
    lang = db.StringField()
    id = db.IntField()
    meta = {'allow_inheritance': True}



