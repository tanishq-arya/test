from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # made for whole class now all methods can access this
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field can't be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                        )

    @jwt_required()  # need to authenticate user before
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occurred finding the item."}, 500

        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
            # 400 => bad request => client error

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            # Internal Server Error
            return {"message": "An error occurred inserting the item."}, 500

        # status code => created is 201
        return item.json(), 201  # so that app knows it is created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):  # idempotent => can be called multiple times
        data = Item.parser.parse_args()

        try:
            item = ItemModel.find_by_name(name)
        except:
            return {"message": "An error occurred finding the item."}, 500

        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                # Internal Server Error
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                item.price = data['price']
            except:
                # Internal Server Error
                return {"message": "An error occurred updating the item."}, 500

        # SQLAlchemy automatically create/ update
        item.save_to_db()

        return item.json()


# new resource
class ItemList(Resource):
    def get(self):
        # we need to return => {'items': items}
        # ItemModel.query.all() => .all() => returns all objects
        # return {
        #     'items':list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {'items': [item.json() for item in ItemModel.query.all()]}
