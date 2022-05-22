from db import db

class StoreModel(db.Model):
    # we need to specify the table name as a variable
    __tablename__ = 'stores'

    # we need to specify the columns of the table
    # any other property of object won't be read/saved to the database
    # id => auto incrementing
    # we can put a UUID as _id for our db manually
    # UUID => Universally Unique Identifier => a very long list of num,char, dashes => unique
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # 1. backrelation from items => store
    # 2. relationship is created => whenever we create a storeModel it will create an object for each item in items table
    # 3. can be expensive operation for many items
    # 4. to prevent this lazy='dynamic' is used
    # 5. create item objects only when .all() is used
    # 6. now it is a query builder that looks into table

    # 7. unless json() is called we don't look into tale => creating tables is simple => .json() is slower
    # --------------------------OR---------------------------------
    # 8. we can create table once => takes time => but .json() is fast

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name) -> None:
        self.name = name

    def json(self):
        return {
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
        }

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
