from db import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(200), unique=True)
    password = db.Column(db.String())
    name = db.Column(db.String(1000))