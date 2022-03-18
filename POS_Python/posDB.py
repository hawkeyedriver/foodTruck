"""Cashier POS"""
import sqlite3
#from typing_extensions import OrderedDict
from restaurant import Restaurant
from menuItem import MenuItem
from order import Order
from item import Items

#Always execute and commit changes to a database
#Always set query in a variable rather in the execute itself

class PosDB:

    def __init__(self):

        self.connection = False
        self.query = "NULL"

        self.currentRName = ""
        self.currentRType = ""
        self.cashierName = ""

        #Display records containing list
        self.recordsRestaurant = list()
        self.recordsMenuItem = list()
        self.recordsMenuItemSub = list()
        self.recordsMenuItemSelect = list()
        self.recordsOrder = list()
        self.recordsItem = list()

        #Lists containing Values to Insert/Update Restaurants
        self.insertRecordRestaurant = ["", "", ""]
        self.updateRecordRestaurant = [0, "", "", ""]
        
        #Lists containing Values to Insert/Update Menu Items
        self.insertRecordMnItm = ["", 0.0, "", "", 0, 0]
        self.updateRecordMnItm = [0, "", 0.0, "", "", 0, 0]

        #Lists containing Values to Insert/Update Orders
        self.insertRecordOrder = [0, 0, 0, 0.0]
        self.updateRecordOrder = [0, 0, 0, 0, 0.0]

        #Lists containing Values to Insert/Update Items
        self.insertRecordItm = [0, 0, 0, "", "", "", 0, 0]
        self.updateRecordItm = [0, 0, 0, 0, "", "", "", 0, 0]

    """Getters and Setters"""

    #Current Restaurant Running
    def getCurrentRName(self):
        return self.currentRName
    def setCurrentRName(self, name):
        self.currentRName = name

    def getCurrentRType(self):
        return self.currentRType
    def setCurrentRType(self, type):
        self.currentRType = type

    #Current Cashier Name
    def getCashierName(self):
        return self.cashierName
    def setCashierName(self, name):
        self.cashierName = name

    """Connection Status Methods"""

    #Establishing Connection
    def connecting(self):
        if(not self.connection):
            try:

                self.dbConnection = sqlite3.connect("foodTruck.db")
                self.dbCursor = self.dbConnection.cursor()
                self.connection = True
                
                self.getRecordsRestaurant()
                
                return "Connected"
        
            except sqlite3.Error as errorDetails:
                print("Error connecting: ", errorDetails)
                return "Disconnected"
        else:
            return "Connected"

    #Destablishing Connection
    def disconnecting(self):
        
        if(self.connection):

            self.dbCursor.close()
            self.dbConnection.close()
            self.connection = False
            print("Disconnect Successful")
            
            return "Disconnected"
        else:
            return "Disconnected"

    '''CRUD for restaurant'''
    #C- Create restaurants
    def createRecordsRestaurant(self):
        
        try:
            self.query = ("INSERT INTO restaurant (storeName, address, restaurantType) VALUES (?,?,?);")
            self.dbCursor.execute(self.query,self.insertRecordRestaurant)
            self.dbConnection.commit()

            self.getRecordsRestaurant()
            
            return "Record Inserted"
        except sqlite3.Error as errorDetails:
            return ("Error Inserting Record: ",errorDetails)

    #R- Read restaurants
    def getRecordsRestaurant(self):
        
        try:
            self.query = "SELECT * FROM restaurant;"
            self.dbCursor.execute(self.query)

            self.middleList = self.dbCursor.fetchall()

            for x in self.middleList:
                print(x)
                (self.id, self.name, self.address, self.type) = x
                self.recordsRestaurant.append(Restaurant(self.id, self.name, self.address, self.type))
            
            return "Records Received"
        except sqlite3.Error as errorDetails:
            return ("Error Receiving Records: ", errorDetails)

    #U- Update restaurants
    def updateRecordsRestaurant(self):
        try:
            self.query = ("UPDATE menuItems SET storeName='"+ self.updateRecordRestaurant[1] + "', address='" 
                                + str(self.updateRecordRestaurant[2]) + "', restaurantType='" + self.updateRecordRestaurant[3]
                                + "' WHERE id=" + str(self.updateRecordRestaurant[0]) + ";")
            self.dbCursor.execute(self.query)
            self.dbConnection.commit()
            return "Record Updated"
        except sqlite3.Error as error:
            return ("Error Updating Record:", error)
    
    #D- Delete restaurants
    def deleteRecordsRestaurant(self, idVal):
        try:
            self.query = "DELETE FROM restaurant WHERE id=" + str(idVal) + ";"
            self.dbCursor.execute(self.query)
            self.dbConnection.commit()

            self.getRecordsRestaurant()
            
            return "Record Deleted"
        except sqlite3.Error as errorDetails:
            return ("Error Deleting Record: ", errorDetails)

    '''CRUD for menuItems'''
    #C- Create menu items
    def createRecordsMenuItems(self):
        
        try:
            self.query = ("INSERT INTO menuItems (itemName, itemPrice, restaurantType, "
                            + "lingoName, foodType, ticketName) VALUES (?,?,?,?,?,?);")
            self.dbCursor.execute(self.query,self.insertRecordMnItm)
            self.dbConnection.commit()

            self.getRecordsMenuItems()
            
            return "Record Inserted"
        except sqlite3.Error as errorDetails:
            return ("Error Inserting Record: ",errorDetails)

    #R- Read menu items
    def getRecordsMenuItemsMain(self, restaurant):
        
        try:
            #WHERE foodType = 2 AND restaurantType=" + str(self.getCurrentR) + ";"
            self.query = "SELECT * FROM menuItems WHERE restaurantType ='" + restaurant + "' AND foodType < 5;"
            self.dbCursor.execute(self.query)

            self.middleList = self.dbCursor.fetchall()

            for x in self.middleList:

                '''Did not like trying to take out 6 items at once 
                from the tuple, so values taken out manually'''
                item = list()

                for y in range(len(x)):
                    item.append(x[y])

                self.recordsMenuItem.append(MenuItem(int(item[0]), item[1], int(item[2]), 
                                                item[3], item[4], int(item[5]), item[6]))
            
            print(len(self.recordsMenuItem))

            return "Records Received"
        except sqlite3.Error as errorDetails:
            return ("Error Receiving Records: ", errorDetails)
    
    #R- Read menu items
    def getRecordsMenuItemsSub(self, restaurant):
        
        try:
            self.query = "SELECT * FROM menuItems WHERE restaurantType ='" + restaurant + "' AND foodType > 4;"
            self.dbCursor.execute(self.query)

            self.middleList = self.dbCursor.fetchall()

            for x in self.middleList:

                '''Did not like trying to take out 6 items at once 
                from the tuple, so values taken out manually'''
                item = list()

                for y in range(len(x)):
                    item.append(x[y])

                self.recordsMenuItemSub.append(MenuItem(int(item[0]), item[1], int(item[2]), 
                                                item[3], item[4], int(item[5]), item[6]))
            
            print(len(self.recordsMenuItemSub))
            
            return "Records Received"
        except sqlite3.Error as errorDetails:
            return ("Error Receiving Records: ", errorDetails)


    #R- Read menu items
    def getRecordsMenuItemsSelect(self, restaurant, food):
        
        try:
            self.query = "SELECT * FROM menuItems WHERE restaurantType ='" + restaurant + "' AND foodType =" + str(food) + ";"
            self.dbCursor.execute(self.query)

            self.middleList = self.dbCursor.fetchall()

            #Resets to allow for new selection
            self.recordsMenuItemSelect = list()

            for x in self.middleList:

                '''Did not like trying to take out 6 items at once 
                from the tuple, so values taken out manually'''
                item = list()

                for y in range(len(x)):
                    item.append(x[y])

                self.recordsMenuItemSelect.append(MenuItem(int(item[0]), item[1], int(item[2]), 
                                                item[3], item[4], int(item[5]), item[6]))
            
            print(len(self.recordsMenuItemSelect))
            
            return "Records Received"
        except sqlite3.Error as errorDetails:
            return ("Error Receiving Records: ", errorDetails)

    #U- Update menu items
    def updateRecordsMenuItems(self):
        try:
            self.query = ("UPDATE menuItems SET itemName='"+ self.updateRecordMnItm[1] + "', itemPrice=" 
                                + str(self.updateRecordMnItm[2]) + ", restaurantType='" + self.updateRecordMnItm[3] 
                                + "', lingoName='" 
                                + self.updateRecordMnItm[4] + "', foodType=" 
                                + str(self.updateRecordMnItm[5]) + ", ticketName='" + self.updateRecordMnItm[6]
                                + "' WHERE id=" + str(self.updateRecordMnItm[0]) + ";")
            self.dbCursor.execute(self.query)
            self.dbConnection.commit()
            return "Record Updated"
        except sqlite3.Error as error:
            return ("Error Updating Record:", error)
    
    #D- Delete menu items
    def deleteRecordsMenuItems(self, idVal):
        try:
            self.query = "DELETE FROM menuItems WHERE id=" + str(idVal) + ";"
            self.dbCursor.execute(self.query)
            self.dbConnection.commit()

            self.getRecordsMenuItems()
            
            return "Record Deleted"
        except sqlite3.Error as errorDetails:
            return ("Error Deleting Record: ", errorDetails)

    """CRUD for Orders"""

    #C- Create orders
    def createRecordsOrder(self):
        
        try:
            print("Enter Orders")
            self.query = "INSERT INTO orders (orderNum, tableNum, status, totalCost) VALUES (?,?,?,?);"
            self.dbCursor.execute(self.query,self.insertRecordOrder)
            self.dbConnection.commit()

            self.getRecordsOrder()
            
            return "Order Inserted"
        except sqlite3.Error as errorDetails:
            return ("Error Inserting Record: ", errorDetails)

    #R- Read orders
    def getRecordsOrder(self):
        
        try:
            self.query = "SELECT * FROM orders;"
            self.dbCursor.execute(self.query)

            self.recordsOrder = self.dbCursor.fetchall()

            return "Records Received"
        except sqlite3.Error as errorDetails:
            return ("Error Receiving Records: ", errorDetails)
        
    def getTableNum(self, orderNum):
        try:
            self.query = "SELECT tableNum FROM orders WHERE orderNum =" + str(orderNum) + " ;"
            self.dbCursor.execute(self.query)

            number = sum(self.dbCursor.fetchone())
            return number
        except sqlite3.Error as errorDetails:
            return ("Error Receiving Records: ", errorDetails)

    #R- Read order by status 
    def getOrdersByStatus(self):
        orderNums = list()
        try:
            self.query = "SELECT orderNum FROM orders WHERE status = 4 or status = 0 or status = 1;"
            self.dbCursor.execute(self.query)

            self.newOrders = self.dbCursor.fetchall()

            for x in self.newOrders:
                orderNums.append(x)
            
            return orderNums
        except sqlite3.Error as errorDetails:
            return ("Error Receiving Records: ", errorDetails)

    #R- Read order by status, return num of frames to be shown
    '''Statuses:
    0- displayed
    1- in Progress
    2- done 
    3- canceled 
    4- not yet shown 
    '''
    def getNumOrderShow(self):
        orders = list()
        try:
            self.query = "SELECT orderNum FROM orders WHERE status = 4 or status = 0 or status = 1;"
            self.dbCursor.execute(self.query)

            self.newOrders = self.dbCursor.fetchall()

            for x in self.newOrders:
                orders.append(x)
            
            return len(orders)
        except sqlite3.Error as errorDetails:
            return ("Error Receiving Records: ", errorDetails)

    def getNewOrderShow(self):
        orders = list()
        try:
            self.query = "SELECT orderNum FROM orders WHERE status = 4;"
            self.dbCursor.execute(self.query)

            self.newOrders = self.dbCursor.fetchall()

            for x in self.newOrders:
                orders.append(sum(x))
            
            return orders
        except sqlite3.Error as errorDetails:
            return ("Error Receiving Records: ", errorDetails)


    #U- Update orders
    def updateRecordsOrder(self, idVal):
        try:
            self.query = ("UPDATE orders SET orderNum="+ str(self.updateRecordOrder[1]) + ", status=" 
                        + str(self.updateRecordOrder[2]) + ", totalCost=" 
                        + str(self.updateRecord[3]) + " WHERE id=" + str(self.updateRecordOrder[0]) + ";")
            self.dbCursor.execute(self.query)
            self.dbConnection.commit()
            return "Record Updated"
        except sqlite3.Error as error:
            return ("Error Updating Record:", error)

    # Update status by order Number 
    def updateStatusOrder(self, order, value):
        try:
            self.query = ("UPDATE orders SET status=" + str(value) + 
                        " WHERE orderNum= " + str(order) + ";")
            self.dbCursor.execute(self.query)
            self.dbConnection.commit()
            return "Record Updated"
        except sqlite3.Error as error:
            return ("Error Updating Record:", error)

    #D- Delete orders
    def deleteRecordsOrder(self, idVal):
        try:
            self.query = "DELETE FROM orders WHERE id=" + str(idVal) + ";"
            self.dbCursor.execute(self.query)
            self.dbConnection.commit()

            self.getRecordsOrder()
            
            return "Record Deleted"
        except sqlite3.Error as errorDetails:
            return ("Error Deleting Record: ", errorDetails)

    '''CRUD for items'''

    #C- Create items
    def createRecordsItm(self):
        try:
            self.query = ("INSERT INTO items (orderNum, tableNum, seatNum, itemName, " 
                        + "comments, lingoName, foodType, status) VALUES (?,?,?,?,?,?,?,?);")
            self.dbCursor.execute(self.query,self.insertRecordItm)
            self.dbConnection.commit()

            self.getRecordsItm()
            
            return "Record Inserted"
        except sqlite3.Error as errorDetails:
            return ("Error Inserting Record: ",errorDetails)

    #R- Read items
    def getRecordsItm(self):
        try:
            self.query = "SELECT * FROM items;"
            self.dbCursor.execute(self.query)

            self.recordsItem = self.dbCursor.fetchall()
            
            return "Records Received"
        except sqlite3.Error as errorDetails:
            return ("Error Receiving Records: ", errorDetails)

    #Reading lingo names by order number and seat
    def getLingoNames(self, orderNumber, seatNum):
        try:
            self.query = "SELECT lingoName FROM items WHERE orderNum= " + str(orderNumber) + " and seatNum= " +str(seatNum) + " and status = 4;"
            self.dbCursor.execute(self.query)
            text = ''
            for x in self.dbCursor.fetchall():
                for y in x:
                    text += " " + y

            return text
        except sqlite3.Error as errorDetails:
            return ("Error Receiving Records: ", errorDetails)
  
    def getItemStatus(self, orderNumber, seatNum):
            try:
                self.query = "SELECT status FROM items WHERE orderNum= " + str(orderNumber) + "and seat= " +str(seatNum) +";"
                self.dbCursor.execute(self.query)
                text = ''
                self.status = self.dbCursor.fetchone()
                return self.status
            except sqlite3.Error as errorDetails:
                return ("Error Receiving Records: ", errorDetails)
  
        

    #U- Update items


    def unshownToShown(self, orderNumber, seat):
        try:
            self.query = ("UPDATE items SET status=0" 
                                + " WHERE orderNum=" + str(orderNumber) + " and seat=" + str(seat) + " ;")
            self.dbCursor.execute(self.query)
            self.dbConnection.commit()
            return "Record Updated"
        except sqlite3.Error as error:
            return ("Error Updating Record:", error)

    def updateStatusItem(self, orderNumber, seat, status):
        try:
            self.query = ("UPDATE items SET status= " + str(status) + " WHERE orderNum=" + str(orderNumber) + " and seatNum=" + str(seat) + " ;")
            self.dbCursor.execute(self.query)
            self.dbConnection.commit()
            return "Record Updated"
        except sqlite3.Error as error:
            return ("Error Updating Record:", error)


    #D- Delete items
    def deleteRecordsItm(self, idVal):
        try:
            self.query = "DELETE FROM items WHERE id=" + str(idVal) + ";"
            self.dbCursor.execute(self.query)
            self.dbConnection.commit()

            self.getRecordsItm()
            
            return "Record Deleted"
        except sqlite3.Error as errorDetails:
            return ("Error Deleting Record: ", errorDetails)
