import datetime
import json
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import UserMixin
from sqlalchemy import create_engine
from web.dbase import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
      
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    products = db.relationship('Product', backref='section', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    section_id =  db.Column(db.Integer, db.ForeignKey('section.id'), nullable=True)
    price = db.Column(db.Integer, default=0)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product = db.Column(db.Integer, nullable=False)
    customer = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=datetime.date.today)


