import json

import pymongo
from flask import Flask
from flask_restful import Resource, Api, abort
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from flask_jwt_extended import  JWTManager

from config import CONNECTION_URL

app = Flask(__name__)
api = Api(app)
app.config.from_pyfile('config.py')

bcrypt = Bcrypt(app)
jwt = JWTManager(app)


client = pymongo.MongoClient("mongodb+srv://flaskuser:wH4j6Fisx4CAvjll@cluster0.3ghec.mongodb.net/")
db = client.test





##
## Actually setup the Api resource routing here
##

from resources.auth import Login, Register
from resources.messages import MessagesList, UnreadMesseages, Message

api.add_resource(MessagesList, '/messages')
api.add_resource(UnreadMesseages, '/messages/unread')
api.add_resource(Message, '/messages/<id>')
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')

@app.route("/")
def home_view():
        return "<h1>Welcome to Messages api</h1>"