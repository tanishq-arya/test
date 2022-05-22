from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
# specify the location of data.db
# "sqlite:///data.db" => it is in root folder
# you can use MySQL, Postgres etc..
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# turn off the flask modification tracker
# SQLAlchemy has it's own tracker which is active
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ** should be secure
app.secret_key = 'jose'

api = Api(app)

# Flask decorator
@app.before_first_request
def create_tables():
  db.create_all() # create all the tables unless they exist already




jwt = JWT(app, authenticate, identity)  # /auth

# this resource is accessible via our api
# how to access ?
# we don't have to mention the decorator
# http://127.0.0.1:5000/student/Rolf
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# endpoints** for store resource
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# new endpoint
api.add_resource(UserRegister, '/register')


# to prevent running app if something is imported from app.py file
if __name__ == '__main__':
    db.init_app(app)
    # debug = True gives html page with for error
    app.run(port=5000, debug=True)
