from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


'''
                                                                   Database Model
'''
class RefrigeratorModel(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ITEM_NAME = db.Column(db.String(50), nullable=False, unique=True)           #Unique so that the resource can be reached via name as well. 
    COUNT_OF_ITEM = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            'ID': self.ID,
            'ITEM_NAME': self.ITEM_NAME,
            'COUNT_OF_ITEM': self.COUNT_OF_ITEM
        }

    def __repr__(self):
        return "Refrigerator(id= {0}, name = {1}, count={2})".format(ID,ITEM_NAME,COUNT_OF_ITEM)

db.create_all()



'''
                                                                Return fields for a single Item (ItemById and ItemByName)
'''

#for marshalling the output data in correct format
resource_item_fields = {
    'ID': fields.Integer,
    'ITEM_NAME': fields.String,
    'COUNT_OF_ITEM': fields.Integer

}



'''
                                                                   ENDPOINT: Item By ID
'''

#for parsing input arguments while creating a single Item
ItemArgumentsByIDForPostMethod = reqparse.RequestParser()
ItemArgumentsByIDForPostMethod.add_argument("item_name", type=str, help="Please send name of the item to be added", required=True)
ItemArgumentsByIDForPostMethod.add_argument("item_count", type=int, help="Please send count of items to be added", required=True)

#for parsing input arguments while updating a single Item
ItemArgumentsByIDForPutMethod = reqparse.RequestParser()
ItemArgumentsByIDForPutMethod.add_argument("differential_item_count", type=int, help="Please send count of items to be added (positive value) or removed (negative value)", required=True)

#Endpoint for Item handling by ID
class ItemByID(Resource):
    # Get existing Item
    @marshal_with(resource_item_fields)
    def get(self, item_id):
        item = RefrigeratorModel.query.filter_by(ID=item_id).first()
        if not item:
            abort(404, message="Item not found.")
        return item

    # Create new item
    @marshal_with(resource_item_fields)
    def post(self, item_id):
        args= ItemArgumentsByIDForPostMethod.parse_args()
        itemIDExists = RefrigeratorModel.query.filter_by(ID=item_id).first()
        itemNameExists= RefrigeratorModel.query.filter_by(ITEM_NAME=args["item_name"]).first()
        if itemIDExists or itemNameExists:                                  # item_name has unique constraint
            abort(404, message="Item already exits.")
        item = RefrigeratorModel(ID=item_id, ITEM_NAME=args["item_name"], COUNT_OF_ITEM=args["item_count"])
        db.session.add(item)
        db.session.commit()
        return item, 201

    # Update Existing Item
    @marshal_with(resource_item_fields)
    def put(self,item_id):
        args= ItemArgumentsByIDForPutMethod.parse_args()
        item = RefrigeratorModel.query.filter_by(ID=item_id).first()
        if not item:
            abort(404, message="Item not found.")
        if args["differential_item_count"]<0 and (item.COUNT_OF_ITEM<args["differential_item_count"]*-1):
            abort(400, message="Requested count of item to be taken out should be less than existing count of item.")
        totalCountOfItem= item.COUNT_OF_ITEM + args["differential_item_count"]
        item.COUNT_OF_ITEM= totalCountOfItem
        if totalCountOfItem==0:
            db.session.delete(item)
        else:
            db.session.add(item)
        db.session.commit()
        return item, 200

    # Delete Item Completely
    def delete(self,item_id):
        item = RefrigeratorModel.query.filter_by(ID=item_id).first()
        if not item:
            abort(404, message="Item not found.")
        db.session.delete(item)
        db.session.commit()
        return '', 204

api.add_resource(ItemByID, "/refrigerator/itemById/<int:item_id>")     


    
'''
                                                                     ENDPOINT: Item By Name
'''
#for parsing input arguments while creating a single Item
ItemArgumentsByNameForPostMethod = reqparse.RequestParser()
ItemArgumentsByNameForPostMethod.add_argument("item_count", type=int, help="Please send count of items to be added", required=True)

#for parsing input arguments while updating a single Item
ItemArgumentsByNameForPutMethod = reqparse.RequestParser()
ItemArgumentsByNameForPutMethod.add_argument("differential_item_count", type=int, help="Please send count of items to be added (positive value) or removed (negative value)", required=True)

#Endpoint for Item handling by Name
class ItemByName(Resource):
    # Get existing Item
    @marshal_with(resource_item_fields)
    def get(self, item_name):
        item = RefrigeratorModel.query.filter_by(ITEM_NAME=item_name).first()
        if not item:
            abort(404, message="Item not found.")
        return item

    # Create new item
    @marshal_with(resource_item_fields)
    def post(self, item_name):
        args= ItemArgumentsByNameForPostMethod.parse_args()
        itemNameExists = RefrigeratorModel.query.filter_by(ITEM_NAME=item_name).first()
        if itemNameExists:                               # item_name has unique constraint
            abort(404, message="Item already exits.")
        item = RefrigeratorModel(ITEM_NAME=item_name, COUNT_OF_ITEM=args["item_count"])       #Automatic ID generation starts from 1
        db.session.add(item)
        db.session.commit()
        return item, 201

    # Update Existing Item
    @marshal_with(resource_item_fields)
    def put(self,item_name):
        args= ItemArgumentsByNameForPutMethod.parse_args()
        item = RefrigeratorModel.query.filter_by(ITEM_NAME=item_name).first()
        if not item:
            abort(404, message="Item not found.")
        if args["differential_item_count"]<0 and (item.COUNT_OF_ITEM<args["differential_item_count"]*-1):
            abort(400, message="Requested count of item to be taken out should be less than existing count of item.")
        totalCountOfItem= item.COUNT_OF_ITEM + args["differential_item_count"]
        item.COUNT_OF_ITEM= totalCountOfItem
        if totalCountOfItem==0:
            db.session.delete(item)
        else:
            db.session.add(item)
        db.session.commit()
        return item, 200

    # Delete Item Completely
    def delete(self,item_name):
        item = RefrigeratorModel.query.filter_by(ITEM_NAME=item_name).first()
        if not item:
            abort(404, message="Item not found.")
        db.session.delete(item)
        db.session.commit()
        return '', 204

api.add_resource(ItemByName, "/refrigerator/itemByName/<string:item_name>") 



'''
                                                                ENDPOINT: All Items
'''
#Endpoint to handle all items in the refrigerator
class AllItems(Resource):

    #displayAllItems
    def get(self):
        items= RefrigeratorModel.query.all()
        return jsonify([RefrigeratorModel.serialize(item) for item in items])
       
    #emptyOutTheRefrigerator
    def delete(self):
        numberOfRowsDeleted= db.session.query(RefrigeratorModel).delete()
        db.session.commit()
        return numberOfRowsDeleted, 204

api.add_resource(AllItems, "/refrigerator/allItems")   



'''
                                                                 Run the app
'''

if __name__== "__main__":
    app.run()