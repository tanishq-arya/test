import sqlite3
from db import db


class UserModel(db.Model):
    # we need to specify the table name as a variable
    __tablename__ = 'users'

    # we need to specify the columns of the table
    # any other property of object won't be read/saved to the database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
