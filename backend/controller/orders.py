from flask import jsonify
from backend.dao.orders import OrderDAO
from backend.dao.user import UserDAO


class OrderController:
    def order_build_dict(self, row):
        result = {}
        result['order_id'] = row[0]
        result['user_id'] = row[1]
        result['total'] = row[2]
        return result

    def orderInfo_build_dict(self, row):
        result = {}
        result['part_id'] = row[0]
        result['part_name'] = row[1]
        result['part_price'] = row[2]
        result['quantity'] = row[3]
        result['partstotal'] = row[4]
        return result

    def newOrder_build_dict(self, row):
        result={}
        result['part_id'] = row[0]
        result['partquantity']= row[1]
        result['price_bought'] = row[2]
        return result

    def getOrderTotal_build_dict(self, row):
        result={}
        result['Order Total'] = row[0]
        return result
    def getOrdersByUser_build_dict(self, row):
        result = {}
        result['order_id'] = row[0]
        result['total'] = row[1]
        result['date'] = row[2]

        return result

    def lastOrderDict(self, row):
        result = {}
        result['order_id'] = row[0]
        return  result

    def getAllOrders(self):
        dao = OrderDAO()

        result_tuples = dao.getAllOrders()
        result = []
        for row in result_tuples:
            dict = self.order_build_dict(row)
            result.append(dict)

        return jsonify(order=result)

    def getOrderInfoById(self, order_id):
        dao = OrderDAO()
        result_tuple = dao.getOrderInfoById(order_id)
        orderTotal = dao.getOrderTotal(order_id)
        if not result_tuple:
            return jsonify("ERROR NOT FOUND"), 404

        result_list = []
        for row in result_tuple:
            result = self.orderInfo_build_dict(row)
            result_list.append(result)
        return jsonify(order = result_list, total = orderTotal)

    def getOrderByUser(self, user_id):
        dao = OrderDAO()
        result_tuple = dao.getOrdersByUserId(user_id)
        if not result_tuple:
            return jsonify("ERROR, NOT FOUND"), 404
        result_list = []
        for row in result_tuple:
            result = self.getOrdersByUser_build_dict(row)
            result_list.append(result)

        return jsonify(result_list)

    def getLastOrder(self, user_id):
        dao = OrderDAO()

        result_tuple = dao.getLastOrder(user_id)

        result_list = []
        for row in result_tuple:
            result = self.lastOrderDict(row)
            result_list.append(result)

        return jsonify(result_list)

    def createOrder(self, user_id):
        dao = OrderDAO()
        result_tuple = dao.createOrder(user_id)
        orderid = dao.getLastOrder(user_id)

        if not result_tuple:
            return jsonify(Error="Order Could not be completed because of balance or stock"), 404
        result_list=[]
        for row in result_tuple:
            result = self.newOrder_build_dict(row)
            resultorder = self.lastOrderDict(orderid)
            result_list.append(result)
            result_list.append(resultorder)
        return jsonify(result_list)

    def deleteOrder(self, json):
        aUser_id = json['Admin ID']
        order_id = json['Order ID']
        dao = OrderDAO()
        userdao = UserDAO()
        admin = userdao.userAdmin(aUser_id)
        print("DELETE ORDER USER ADMIN ", admin)
        if admin:
            result_tuple = dao.deleteOrder(order_id)
            if not result_tuple:
                return jsonify(Error = "NO ORDER FOUND"),404
            elif result_tuple:
                return jsonify("ORDER ", result_tuple, " DELETED FROM RECORD"), 200
        elif not admin:
            return jsonify(Error = "NOT ADMIN"), 404



