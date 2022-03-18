"""Class Object to Organize and Easily access
Record Field data, 'orders' table"""
class Order:

    orderId = 0
    orderNum = 0
    tableNum = 0
    status = 0
    totalCost = 0.0

    #Constructor
    def __init__(self, id, num, table, status, cost):
        self.orderId = id
        self.orderNum = num
        self.tableNum = table
        self.status = status
        self.totalCost = cost

    """Getters and Setters"""

    #Id
    def getId(self):
        return self.orderId
    def setId(self, id):
        self.orderId = id

    #Order Number
    def getOrderNum(self):
        return self.orderNum
    def setOrderNum(self, num):
        self.orderNum = num

    #Table Number
    def getTableNum(self):
        return self.tableNum
    def setTableNum(self, table):
        self.tableNum = table

    #Status
    def getStatus(self):
        return self.status
    def setStatus(self, status):
        self.status = status

    #Total
    def getTotalCost(self):
        return self.totalCost
    def setTotalCost(self, cost):
        self.totalCost = cost
