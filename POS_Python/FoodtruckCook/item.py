"""Class Object to Organize and Easily access
Record Field data, 'items' table"""
class Items:

    itemId = 0
    orderNum = 0
    tableNum = 0
    seatNum = 0
    itemName = ""
    comments = ""
    lingoName = ""
    foodType = 0
    status = 0

    price = 0

    #Constructor
    def __init__(self, id, num, table, seat, name, comment, lingo, type, status):
        self.itemId = id
        self.orderNum = num
        self.itemName = name
        self.tableNum = table
        self.seatNum = seat
        self.comments = comment
        self.lingoName = lingo
        self.foodType = type
        self.status = status

        self.price = 0

    """Getters and Setters"""

    #Id
    def getId(self):
        return self.itemId
    def setId(self, id):
        self.itemId = id

    #Order Number
    def getOrderNum(self):
        return self.orderNum
    def setOrderNum(self, num):
        self.orderNum = num

    #Item Name
    def getItemName(self):
        return self.itemName
    def setItemName(self, name):
        self.itemName = name

    #Seat Number
    def getSeatNum(self):
        return self.seatNum
    def setSeatNum(self, seat):
        self.seatNum = seat

    #Table Number
    def getTableNum(self):
        return self.tableNum
    def setTableNum(self, table):
        self.tableNum = table
    
    #Comment
    def getComments(self):
        return self.comments
    def setComments(self, comment):
        self.comments = comment

    #Lingo Name, Kitchen Nickname
    def getLingoName(self):
        return self.lingoName
    def setLingoName(self, lingo):
        self.lingoName = lingo

    #Food Type
    def getFoodType(self):
        return self.foodType
    def setFoodType(self, type):
        self.foodType = type

    #Status
    def getStatus(self):
        return self.status
    def setStatus(self, status):
        self.status = status
