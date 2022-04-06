from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from controller.orders import OrderController
from controller.parts import PartController
from controller.user import UserController

app = Flask(__name__)

'''Root route for handler() function.'''


@app.route('/')
def handler():
    return 'Root route. Hello, user!'


"""
    All parts in the page. 
"""


@app.route('/PartsApp/Parts', methods=['GET', 'POST', 'DELETE'])
def parts_handler():
    if request.method == 'GET':
        return PartController().getAllParts()
    elif request.method == 'POST':
        return PartController().newPart(request.json)
    else:
        return jsonify("Method Not Supported"), 405


"""
    Page for part with specific part id.
"""


@app.route('/PartsApp/Parts/<int:part_id>', methods=['GET', 'PUT', 'DELETE'])
def parts_byid_handler(part_id):
    if request.method == 'GET':
        return PartController().getPartById(part_id)
    elif request.method == 'PUT':
        return PartController().updatePart(part_id, request.json)
    elif request.method == 'DELETE':
        return PartController().deletePart(part_id)
    else:
        return jsonify("Not Supported"), 405


"""
    Parts page for specified category of the part. 
"""


@app.route('/PartsApp/Parts/<string:cat_name>', methods=['GET'])
def parts_bycatname_handler(cat_name):
    if request.method == 'GET':
        return PartController().getPartByCatname(cat_name)

    else:
        return jsonify("NOT SUPPORTED"), 405


"""
    Route to filter parts by prices less than or equal to desired price.
"""


@app.route('/PartsApp/Parts/Filter/PriceLessThan/<string:part_price>', methods=['GET'])
def parts_by_price_less_than_equal_to(part_price):
    if request.method == 'GET':
        return PartController().getPartsByPriceLessThanOrEqualTo(part_price)
    else:
        return jsonify("NOT SUPPORTED"), 405


"""
    Route to access parts ordered alphabetically (A-Z).
"""


@app.route('/PartsApp/Parts/Ordered', methods=['GET'])
def parts_by_name_ascending():
    if request.method == 'GET':
        return PartController().order_parts_by_name()
    else:
        return jsonify("NOT SUPPORTED"), 405


"""
    Route to get all users
"""


@app.route('/PartsApp/User', methods=['GET', 'POST', 'PUT'])
def user_handler():
    if request.method == 'GET':
        return UserController().getAllUser()
    elif request.method == 'POST':
        return UserController().newUser(request.json)
    elif request.method == 'PUT':
        return UserController().updateUser(request.json)
    else:
        return jsonify("Method Not Supported"), 405




"""
    Route to get all orders
"""

@app.route('/PartsApp/Order', methods = ['GET', 'PUT'])
def order_handler():
    if request.method == 'GET':
        return OrderController().getAllOrders()

    else:
        return jsonify("Method Not Supported"), 405


if __name__ == '__main__':
    app.run(debug=1)
