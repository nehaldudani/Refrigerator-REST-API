# Refrigerator-REST-API

This is a simple Refrigerator REST API. It has three endpoints:

1) To manipulate a single item by ID: "/refrigerator/itemById/<int:item_id>"
2) To manipulate a single item by Name: "/refrigerator/itemByName/<string:item_name>"
3) To manipulate all items in the refrigerator: "/refrigerator/allItems"

1) itemByID: This has GET, POST, PUT and DELETE methods. 
    a) GET is used to access an item by its id. 
       It requires no data in request body
    b) POST is used to create a new item by id.
       -It requires two key value pairs as data in the request body {"item_name": <string>, "item_count": <int>}. Both keys are required otherwise it is a bad request. 
       -The method aborts if item already exists. This is true if either the id already exists or the name of the item already exists.
    c) PUT is used to update an existing item by id.
       -It requires one key value pairs as data in the request body {"differential_item_count": <int>}. This key specifies the count of the item to be added (positive value) or removed (negative value) from the existing total count of the item. This is a required key, value pair. 
            -If this differential_item_count is a positive value: It is simply added to the existing count.
            -If this differential_item_count is a negative value: It is checked if this count can be taken out of the existing count or not. If not, method aborts error message. If yes, this required count is taken out. If the resulting value after taking differential count out is 0, the item is deleted from the refrigerator.
       -The method aborts if item does not exists by id.
    d) DELETE completely deletes a particular item by id from the refrigerator.

2) itemByName: This has GET, POST, PUT and DELETE methods. The refrigerator resource can only have unique names of items.
    a) GET is used to access an item by its name. 
       It requires no data in request body
    b) POST is used to create a new item by name.
       -It requires one key value pair as data in the request body {"item_count": <int>}. This key value pair is required otherwise it is a bad request. 
       -The method aborts if item already exists by name.
    c) PUT is used to update an existing item by name.
       -It requires one key value pairs as data in the request body {"differential_item_count": <int>}. his key specifies the count of the item to be added (positive value) or removed (negative value) from the existing total count of the item. This is a required key, value pair. 
            -If this differential_item_count is a positive value: It is simply added to the existing count.
            -If this differential_item_count is a negative value: It is checked if this count can be taken out of the existing count or not. If not, method aborts error message. If yes, this required count is taken out. If the resulting value after taking differential count out is 0, the item is deleted from the refrigerator.
       -The method aborts if item does not exists by name.
    d) DELETE completely deletes a particular item by name from the refrigerator.

3) allItems: This has GET and DELETE methods
    a) GET is used to get all items in the refrigerator.
    b) DELETE is used to completely empty out the refrigerator.


  To RUN and TEST this APP:

A sample Client is provided with variety of combination of all endpoints and methods. 

1) The following modules must be installed on the system- flask, flask_restful, flask_sqlalchemy, requests

On Mac OS with python3 the command are:

pip3 install flask
pip3 install flask_restful
pip3 install flask_sqlalchemy
pip3 install requests

2) open two terminals:
    a) in the first terminal, start the RestRefrigeratorServer.py python file. This is the REST API endpoint.
    b) in the second terminal, start the RestRefrigeratorClient.py python file. This is a sample client that connects and uses the endpoints provided above.


  FUTURE POSSIBLE MODIFICATIONS: 

1) It is possible to split up the server file. With separate files for the DB model and each endpoint. This is a good practice as the size of a project increases.
2) Add POST and PUT methods in allItems endpoint with a possibility to create and upadte several items together. 
