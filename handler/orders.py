from flask import jsonify
from dao.orders import OrdersDAO


class OrdersHandler:
    def build_order_dict(self, row):
        result = {}
        result['odid'] = row[0]
        result['odnumber'] = row[1]
        return result

    def build_consumer_dict(self, row):
        result = {}
        result['consid'] = row[0]
        result['consusername'] = row[1]
        return result

    def build_reservation_dict(self, row):
        result = {}
        result['resid'] = row[0]
        result['restime'] = row[1]
        return result

    def build_supplier_dict(self, row):
        result = {}
        result['sid'] = row[0]
        result['susername'] = row[1]
        result['sccompany'] = row[2]
        return result

    def build_order_attributes(self, odid, odnumber):
        result = {}
        result['odid'] = odid
        result['odnumber'] = odnumber
        return result

    def getAllOrders(self):
        dao = OrdersDAO()
        order_list = dao.getAllOrders()
        result_list = []
        for row in order_list:
            result = self.build_order_dict(row)
            result_list.append(result)
        return jsonify(Order=result_list)

    def getOrdersById(self, odid):
        dao = OrdersDAO()
        row = dao.getOrdersById(odid)
        if not row:
            return jsonify(Error="Order Not Found"), 404
        else:
            order = self.build_order_dict(row)
        return jsonify(Order=order)

    def searchOrders(self, args):
        odnumber = args.get('odnumber')
        dao = OrdersDAO()
        order_list = []
        if (len(args) == 1) and odnumber:
            order_list = dao.getOrdersByNumber(odnumber)
        else:
            return jsonify(Error="Malformed query string"), 400
        result_list = []
        for row in order_list:
            result = self.build_order_dict(row)
            result_list.append(result)
        return jsonify(Order=result_list)

    def getConsumerByOrdersId(self, odid):
        dao = OrdersDAO()
        if not dao.getOrdersById(odid):
            return jsonify(Error="Order Not Found"), 404
        consumer_list = dao.getConsumerByOrdersId(odid)
        result_list = []
        for row in consumer_list:
            result = self.build_consumer_dict(row)
            result_list.append(result)
        return jsonify(Order=result_list)

    def getReservationByOrdersId(self, odid):
        dao = OrdersDAO()
        if not dao.getOrdersById(odid):
            return jsonify(Error="Order Not Found"), 404
        reservation_list = dao.getReservationByOrdersId(odid)
        result_list = []
        for row in reservation_list:
            result = self.build_reservation_dict(row)
            result_list.append(result)
        return jsonify(Order=result_list)

    def getSupplierByOrdersId(self, odid):
        dao = OrdersDAO()
        if not dao.getOrdersById(odid):
            return jsonify(Error="Order Not Found"), 404
        supplier_list = dao.getSupplierByOrdersId(odid)
        result_list = []
        for row in supplier_list:
            result = self.build_supplier_dict(row)
            result_list.append(result)
        return jsonify(Order=result_list)

    def insertOrdersJson(self, json):
        odnumber = json['odnumber']
        if odnumber:
            dao = OrdersDAO()
            odid = dao.insert(odnumber)
            result = self.build_order_attributes(odid, odnumber)
            return jsonify(Order=result), 201
        else:
            return jsonify(Error="Unexpected attributes in post request"), 400

    def updateOrders(self, odid, form):
        dao = OrdersDAO()
        if not dao.getOrdersById(odid):
            return jsonify(Error="Order not found."), 404
        else:
            if len(form) != 1:
                return jsonify(Error="Malformed update request"), 400
            else:
                odnumber = form['odnumber']
                if odnumber:
                    dao.update(odid, odnumber)
                    result = self.build_order_attributes(odid, odnumber)
                    return jsonify(Order=result), 200
                else:
                    return jsonify(Error="Unexpected attributes in update request"), 400

    def deleteOrders(self, odid):
        dao = OrdersDAO()
        if not dao.getOrdersById(odid):
            return jsonify(Error="Order not found."), 404
        else:
            dao.delete(odid)
            return jsonify(DeleteStatus="OK"), 200