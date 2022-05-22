from db import db


class ItemModel(db.Model):
    # we need to specify the table name as a variable
    __tablename__ = 'items'

    # we need to specify the columns of the table
    # any other property of object won't be read/saved to the database
    # id => auto incrementing
    # we can put a UUID as _id for our db manually
    # UUID => Universally Unique Identifier => a very long list of num,char, dashes => unique
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # Items =====> Store [many to one]
    # We can't delete items unless store id is removed

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')  # sees the store has an id
    # matches the id to stores table

    def __init__(self, name, price, store_id) -> None:
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # ItemModel => type of SQLAlchemy model
        # query => we need to query the model
        # Now SQLAlchemy knows we're building a query
        # multiple => .filter_by().filter_by()
        # filter_by().first() => returns one row only

        # [SELECT * FROM items WHERE name=name]**
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        # Can directly transform object into row
        # Session => collection of objects that we need to insert ot db
        # Can do multiple at one time => depends on time & requirement

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
