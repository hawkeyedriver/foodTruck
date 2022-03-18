"""Class Object to Organize and Easily access
Record Field data, 'restaurant' table"""
class Restaurant:

    restaurantId = 0
    storeName = ""
    address = ""
    restaurantType = ""

    #Constructor
    def __init__(self, id, name, address, type):
        self.restaurantId = id
        self.storeName = name
        self.address = address
        self.restaurantType = type

    """Getters and Setters"""

    #Id
    def getId(self):
        return self.restaurantId
    def setId(self, id):
        self.restaurantId = id

    #Store Name
    def getStoreName(self):
        return self.storeName
    def setStoreName(self, name):
        self.storeName = name

    #Address
    def getAddress(self):
        return self.address
    def setAddress(self, address):
        self.address = address

    #Restaurant Type
    def getRestaurantType(self):
        return self.restaurantType
    def setRestaurantType(self, type):
        self.restaurantType = type
