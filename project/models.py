#from flask_login import UserMixin
#from . import db

#class User(UserMixin, db.Model):
    #id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    #email = db.Column(db.String(100), unique=True)
    #password = db.Column(db.String(100))
    #name = db.Column(db.String(1000))


from flask_login import UserMixin
from datastore_entity import DatastoreEntity, EntityValue
import datetime


class User(DatastoreEntity, UserMixin):
    email = EntityValue(None)
    password = EntityValue(None)
    name = EntityValue(None)
    status = EntityValue(1)
    date_created = EntityValue(datetime.datetime.utcnow())
