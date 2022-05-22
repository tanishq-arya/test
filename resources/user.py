import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank!"
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field can't be blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        # the api doesn't care how the database is implemented
        # it's focus is on the functionality
        # as we have save_to_db in UserModel we can use it.
        # **data => unpacking the data as params for __init__
        user = UserModel(**data)
        user.save_to_db()

        # 201 means created
        return {"message": "User created successfully."}, 201
