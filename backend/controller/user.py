from flask import jsonify
from backend.dao.user import UserDAO


class UserController(object):

    def build_user_dict(self, row):
        result = {}
        result['user_id'] = row[0]
        result['user_password'] = row[1]
        result['user_email'] = row[2]
        result['full_name'] = row[3]
        result['balance'] = row[4]
        result['user_rol'] = row[5]
        return result

    #statistics dict

    def topPartBoughtByUser_build_dict(self, row):
        result = {}
        result['part_name'] = row[0]
        result['part_id'] = row[1]
        result['bought'] = row[2]
        return result

    def topCatBoughtByUser_build_dict(self, row):
        result = {}
        result['cat_id'] = row[0]
        result['category'] = row[1]
        result['bought'] = row[2]
        return result

    def mostExpensivePartUser_build_dict(self, row):
        result = {}
        result['part_id'] = row[0]
        result['part_name'] = row[1]
        result['price'] = row[2]
        return result

    def getAllUser(self):
        dao = UserDAO()

        result_tuples = dao.getAllUser()
        result = []
        for row in result_tuples:
            res = self.build_user_dict(row)
            result.append(res)

        return jsonify(User=result)

    def getUserById(self, user_id):
        dao = UserDAO()

        row = dao.getUserById(user_id)
        if not row:
            return jsonify(Error="No Such User Found"), 404
        else:
            user = self.build_user_dict(row)
        return jsonify(user)

    def newUser(self, json: dict):
        #aUser_id = json['Admin ID']
        user_password = json['user_password']
        user_email = json['user_email']
        full_name = json['full_name']
        balance = json['balance']
        user_rol = False
        dao = UserDAO()
        admin = True
        if admin:
            result = dao.newUser(user_password, user_email, full_name, balance, user_rol)
            if result:
                user_id = result
                return jsonify({
                'user_id': user_id,
               'user_password': user_password,
              'user_email': user_email,
              'full_name': full_name,
              'balance': balance,
              'user_rol': user_rol
             }), 200
        else:
            return jsonify(Error='User does not have access to create accounts'), 406

    def updateUser(self, json: dict):
        aUser_id = json['admin_id']
        user_id = json ['user_id']
        user_password = json['user_password']
        user_email = json['user_email']
        full_name = json['full_name']
        balance = json['balance']
        user_rol = json['user_rol']

        dao = UserDAO()

        admin = dao.userAdmin(aUser_id)

        print("UPDATE USER ADMIN : ", admin)

        result = dao.updateUser(user_id, user_password, user_email, full_name, balance, user_rol)
        if result & admin:
            return jsonify({
                'user_id': user_id,
                'user_password': user_password,
                'user_email': user_email,
                'full_name': full_name,
                'balance': balance,
                'user_rol': user_rol
            }), 200
        else:
            return jsonify(Error='Unable to Update User'), 404

    def deleteUserById(self, json):
        dao = UserDAO()
        user_id = json['user_id']
        aUser_id = json['Admin ID']

        admin = dao.userAdmin(aUser_id)

        if admin:
            result = dao.deleteUserById(user_id)
            if result:
                return jsonify(Error="User Has Been Successfully Deleted"), 200
            if not result:
                return jsonify(Error = "USER NOT FOUND"), 404
        else:
            return jsonify(Error="No Such User Found or Not Admin"), 404

    # statistics
    def getMostBoughtPartUser(self, user_id):
        dao = UserDAO()

        result_tuples = dao.getMostBoughtPartUser(user_id)
        result = []
        for row in result_tuples:
            dict = self.topPartBoughtByUser_build_dict(row)
            result.append(dict)
        return jsonify(result)

    def getMostBoughtCategoryUser(self, user_id):
        dao = UserDAO()

        result_tuples = dao.getMostBoughtCategoryUser(user_id)
        result = []
        for row in result_tuples:
            dict = self.topCatBoughtByUser_build_dict(row)
            result.append(dict)
        return jsonify(result)

    def getMostExpensivePartUser(self, user_id):
        dao = UserDAO()
        result_tuples = dao.getMostExpensivePartUser(user_id)
        result = []
        for row in result_tuples:
            res = self.mostExpensivePartUser_build_dict(row)
            result.append(res)

        return jsonify(result)

    def getCheapestPartUser(self, user_id):
        dao = UserDAO()
        result_tuples = dao.getCheapestPartUser(user_id)
        result = []
        for row in result_tuples:
            res = self.mostExpensivePartUser_build_dict(row)
            result.append(res)

        return jsonify(result)

    #new def for frontend
    def get_acc_by_email_and_password(self,json):
        user_email = json['user_email']
        user_password = json['user_password']
        method = UserDAO()
        user_tuple = method.get_acc_by_email_and_password(user_email, user_password)
        if not user_tuple:
            return jsonify("Not Found"), 404
        else:
            return jsonify({
                'user_email': user_tuple[0],
                'user_password': user_tuple[1],
                'user_id': user_tuple[2],
                'user_rol': user_tuple[3]
            }), 200