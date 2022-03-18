"""Class Object to Organize and Easily access
Record Field data, 'menuItems' table"""
class MenuItem:

    mnitId = 0
    itemName = ""
    itemPrice = 0.0
    restaurantType = ""
    lingoName = ""
    foodType = 0
    ticketName = ""

    #Constructor
    def __init__(self, id, name, price, type, lingo, food, ticket):
        self.mnitId = id
        self.itemName = name
        self.itemPrice = price
        self.restaurantType = type
        self.lingoName = lingo
        self.foodType = food
        self.ticketName = ticket

    """Getters and Setters"""

    #Id
    def getId(self):
        return self.mnitId
    def setId(self, id):
        self.mnitId = id

    #Item Name
    def getItemName(self):
        return self.itemName
    def setItemName(self, name):
        self.itemName = name

    #Item Price
    def getItemPrice(self):
        return self.itemPrice
    def setItemPrice(self, price):
        self.itemPrice = price

    #Restaurant Type
    def getRestaurantType(self):
        return self.restaurantType
    def setRestaurantType(self, type):
        self.restaurantType = type

    #Lingo Name, Kitchen Nickname
    def getLingoName(self):
        return self.lingoName
    def setLingoName(self, lingo):
        self.lingoName = lingo

    #Food Type
    def getFoodType(self):
        return self.foodType
    def setFoodType(self, food):
        self.foodType = food

    #Ticket Name
    def getTicketName(self):
        return self.ticketName
    def setTicketName(self, ticket):
        self.ticketName = ticket
