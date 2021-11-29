from db import db
from typing import List
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, create_access_token

from security import authenticate
from resources.user import UserRegister
from resources.item import ItemList, Item


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config["JWT_SECRET_KEY"] = "super-secret"

api = Api(app)

jwt = JWTManager(app)  # /auth


class Authentication(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        authUser = authenticate(username, password)
        return {'token': create_access_token(identity=authUser['id'])}


api.add_resource(Authentication, '/auth')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=3333, debug=True)
