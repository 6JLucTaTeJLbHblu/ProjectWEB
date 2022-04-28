from flask_login import UserMixin
from . import db
import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Chats(db.Model):
    __tablename__ = 'chats'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'))

class Messages(db.Model):
    __tablename__ = 'messages'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    chat = db.Column(db.Integer, db.ForeignKey('chats.id'))
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(1000))