"""Run in VSCode"""

from cashierPos import CashierApp
from loginPos import LoginRestaurantApp
from posDB import PosDB

def main():

    connection = PosDB()
    connection.connecting()
    login = LoginRestaurantApp(connection)
    print("Restaurant " + connection.getCurrentRType())
    print("Cashier " + connection.getCashierName())

    print(connection.connection)
    if (connection.connection):
        sessionStart = CashierApp(connection)

if (__name__=="__main__"):
    main()
