"""Cashier POS"""
import tkinter as tk
from tkinter import messagebox
from item import Items
import decimal
import sys
import os
import random

class CashierApp:
    def __init__(self, database):

        self.database = database

        #Holds data about current order and items
        self.currentOrder = 1
        self.currentTable = 0

        #Items to be pushed and processing them
        self.listItems = list()
        self.inProgress = False
        self.duplicateIndex = 0

        #Canvas Item lists
        self.clearHeaderTags = list()
        self.clearFoodTags = list()
        self.tagYPos = list()
        self.tags = list()

        #List for Ticket Print
        self.ticketList = list()

        
        #Overall Cost
        self.totalCost = 0.0


        if (not self.database.connection):
            tk.messagebox.showinfo("Error", "Issue Connecting to Database. Ending Program Now. " + 
                                    "Please check that all files are correct and try again.")
        else:
            print("Connected")

            #Main Window
            self.mainwindow = tk.Tk()
            self.mainwindow.title("Cashier POS")
            
            """Menu Setup"""
            
            #Menu Bar
            self.cashierMenu = tk.Menu(self.mainwindow)

            #Menus
            self.fileMenu = tk.Menu(self.cashierMenu, tearoff = 0)
            self.connectionMenu = tk.Menu(self.cashierMenu, tearoff = 0)
            self.helpMenu = tk.Menu(self.cashierMenu, tearoff = 0)

            '''Menu Items'''

            self.fileMenu.add_command(label="Exit", command=lambda: self.mainwindow.destroy())
            
            #Deals with the connection to the database
            self.connectionMenu.add_command(label="Connect")
            self.connectionMenu.add_command(label="Disconnect")

            #About
            self.helpMenu.add_command(label="About",
                                        command=lambda: tk.messagebox.showinfo("About",
                                                            "App that connects to a database and functions "
                                                            +"as the cashier side of a POS system"))

            '''Menu Configs'''

            #Adding all Menu Items to Menu
            self.cashierMenu.add_cascade(label="File", menu=self.fileMenu)
            self.cashierMenu.add_cascade(label="Connection", menu=self.connectionMenu)
            self.cashierMenu.add_cascade(label="Help", menu=self.helpMenu)

            #Configuring Menu to the Window
            self.mainwindow.config(menu=self.cashierMenu)

            #Frame
            self.frameCashierSide = tk.Frame(self.mainwindow, background='#c7d9e1',
                                            height=675, takefocus=False, width=1025)

            """Components"""

            '''Canvas Configs and Scroll Setting'''

            #Canvas, Display Ticket Contents
            self.canvasTicket = tk.Canvas(self.frameCashierSide, background='#a3bdfb', borderwidth=10,
                                        height=535, width=330, insertborderwidth='0', relief='ridge')

            #Setup scroll bar
            self.ticketScrollY = tk.Scrollbar(self.frameCashierSide, orient='vertical', command=self.canvasTicket.yview)
            self.ticketScrollY.place(anchor='nw', height=530, width=10, x=340, y=20)
            
            #Sync scroll and canvas
            self.canvasTicket.configure(yscrollcommand=self.ticketScrollY.set,
                                        yscrollregion = self.canvasTicket.bbox("all"))
            
            self.canvasTicket.place(anchor='nw', relx='0.01', rely='0.0', x='0', y='8')

            #Position of text on canvas
            self.posY = 30
            
            '''Formats Input from Text Boxes to be printed'''

            #Customer Name
            self.cashierText = "Cashier: " + self.database.getCashierName()

            #Given a tag so it can be removed later without complete wipeout
            self.canvasTicket.create_text(175, self.posY, anchor=tk.CENTER,
                                    text=self.database.getCurrentRName(), fill="black", font=('Helvetica 22'))
            self.posY = self.posY + 35
            self.canvasTicket.create_text(20, self.posY, anchor='w',
                                    text=self.cashierText, fill="black", font=('Helvetica 16'))
            self.posY = self.posY + 70
            self.canvasTicket.create_text(170, self.posY,
                                    text="~~~~~~~~~~~~~~~~~~~~~~~~~~~~", fill="black", font=('Helvetica 14'))
            self.posY = self.posY + 32

            """Text Fields"""

            #Customer Name
            self.txtCustomer = tk.Entry(self.frameCashierSide, font='{Verdana} 14 {}', borderwidth='2', relief="sunken")
            self.txtCustomer.place(anchor='nw', height=35, width=175, x=630, y='40')

            #Table Number
            self.txtTable = tk.Entry(self.frameCashierSide, font='{Verdana} 14 {}', borderwidth='2', relief="sunken")
            self.txtTable.place(anchor='nw', height=35, width=50, x=945, y=40)

            #Food Alteration Comments
            self.txtComments = tk.Text(self.frameCashierSide, borderwidth='2', font='{Verdana} 12 {}',
                                    height='10', relief='sunken', width='50')
            self.txtComments.place(anchor='nw', bordermode='inside', height='65', width='350', x='600', y='445')

            """Labels"""

            #Customer Name, Indicates Field Purpose in Window
            self.lblCustomer = tk.Label(self.frameCashierSide, background='#c7d9e1',
                                        font='{Verdana} 20 {}', text='Customer Name:')
            self.lblCustomer.place(anchor='nw', x=385, y='40')

            #Table Num, Indicates Field Purpose in Window
            self.lblTable = tk.Label(self.frameCashierSide, background='#c7d9e1',
                                        font='{Verdana} 20 {}', text='Table:')
            self.lblTable.place(anchor='nw', x=845, y='40')

            #Food Alteration Comments, Indicates Field Purpose in Window
            self.lblComments = tk.Label(self.frameCashierSide, background='#c7d9e1', compound='top',
                                        font='{Verdana} 20 {}', text='Comments:')
            self.lblComments.place(anchor='nw', x='420', y='445')

            #Display Total Label
            self.lblTotal = tk.Label(self.frameCashierSide, background='#c7d9e1', font='{verdana} 16 {}',
                                    justify='center', text='Total: $Lots of Munz')
            self.lblTotal.place(anchor='nw', width=350, x=10, y=600)

            """Buttons"""

            '''Radio Buttons'''

            #~~~Food Toggle Options~~~
            self.strFood = tk.StringVar(value='')

            self.xPosBtn = 415
            self.yPosBtn = 115
            print(self.database.getRecordsMenuItemsMain(self.database.getCurrentRType()))

            self.optionsList = list()
            if (len(self.database.recordsMenuItem) == 0):
                 tk.messagebox.showinfo("Error", "Issue Connecting to Database. Ending Program Now. " 
                                        + "Please check that all files are correct and try again.")
                 self.mainwindow.destroy()
                 sys.exit(1)

            #Gets Menu Items, adds them to list to determine radio button options
            for y in range(len(self.database.recordsMenuItem)):

                #Adds food type to list if val isnt already appended
                if (self.database.recordsMenuItem[y].getFoodType() not in self.optionsList):
                    self.optionsList.append(self.database.recordsMenuItem[y].getFoodType())
                    print(self.optionsList[len(self.optionsList) -1])
                    
            self.btnFoodList = list()
            
            for x in range(len(self.optionsList)):

                #Checks index to shift to column two
                if (x == 3):
                    self.xPosBtn = 575
                    self.yPosBtn = 115

                '''Choose Button Settings'''

                #Appetizers
                if (self.optionsList[x] == 0):
                    self.btnFoodList.append(tk.Radiobutton(self.frameCashierSide, background='#c7d9e1', font='{verdana} 14 {}',
                                        text='Appetizer', variable=self.strFood, value=x, command=lambda: self.buttonPress(0)))
                    self.btnFoodList[x].place(anchor='nw', x=self.xPosBtn, y=self.yPosBtn)

                #Entrees
                elif (self.optionsList[x] == 1):
                    self.btnFoodList.append(tk.Radiobutton(self.frameCashierSide, background='#c7d9e1', font='{verdana} 14 {}',
                                            text='Entree', variable=self.strFood, value=x, command=lambda: self.buttonPress(1)))
                    self.btnFoodList[x].place(anchor='nw', x=self.xPosBtn, y=self.yPosBtn)

                #Sides
                elif (self.optionsList[x] == 2):
                    self.btnFoodList.append(tk.Radiobutton(self.frameCashierSide, background='#c7d9e1', font='{verdana} 14 {}',
                                        text='Side', variable=self.strFood, value=x, command=lambda: self.buttonPress(2)))
                    self.btnFoodList[x].place(anchor='nw', x=self.xPosBtn, y=self.yPosBtn)

                #Desserts
                elif (self.optionsList[x] == 3):
                    self.btnFoodList.append(tk.Radiobutton(self.frameCashierSide, background='#c7d9e1',
                                            font='{verdana} 14 {}', text='Dessert', variable=self.strFood, 
                                            value=x, command=lambda: self.buttonPress(3)))
                    self.btnFoodList[x].place(anchor='nw', x=self.xPosBtn, y=self.yPosBtn)

                #Drinks
                else:
                    self.btnFoodList.append(tk.Radiobutton(self.frameCashierSide, background='#c7d9e1', font='{verdana} 14 {}',
                    text='Drink', variable=self.strFood, value=x, command=lambda: self.buttonPress(4)))
                    self.btnFoodList[x].place(anchor='nw', x=self.xPosBtn, y=self.yPosBtn)
                    
                self.yPosBtn = self.yPosBtn + 30

            #~~~Seat Toggle Options~~~
            self.strSeat = tk.StringVar(value="")

            #Seat One
            self.btnSOne = tk.Radiobutton(self.frameCashierSide, background='#c7d9e1', font='{verdana} 14 {}',
                                        text='Seat One', variable=self.strSeat, value=1, command=lambda: self.setSeat(1))
            self.btnSOne.place(anchor='nw', x='850', y='115')

            #Seat Two
            self.btnSTwo = tk.Radiobutton(self.frameCashierSide, background='#c7d9e1', font='{verdana} 14 {}',
                                        text='Seat Two', variable=self.strSeat, value=2, command=lambda: self.setSeat(2))
            self.btnSTwo.place(anchor='nw', x='850', y='145')

            #Seat Three
            self.btnSThree = tk.Radiobutton(self.frameCashierSide, background='#c7d9e1', font='{verdana} 14 {}',
                                            text='Seat Three', variable=self.strSeat, value=3, command=lambda: self.setSeat(3))
            self.btnSThree.place(anchor='nw', x='850', y='170')

            #Seat Four
            self.btnSFour = tk.Radiobutton(self.frameCashierSide, background='#c7d9e1', font='{verdana} 14 {}',
                                        text='Seat Four', variable=self.strSeat, value=4, command=lambda: self.setSeat(4))
            self.btnSFour.place(anchor='nw', x='850', y='195')

            #~~~Dessert-Specific Subcolumn Options~~~
            self.strDessertType = tk.StringVar(value='')

            self.optionsSubList = list()

            self.yPosBtn = 115

            self.btnFoodSubList = []

            #Checks to see if only has one category to add subcategories
            if (len(self.optionsList) == 1 and self.optionsList[0] == 4):

                print(self.database.getRecordsMenuItemsSub(self.database.getCurrentRType()))

                for y in range(len(self.database.recordsMenuItemSub)):
                    if (self.database.recordsMenuItemSub[y].getFoodType() not in self.optionsSubList):
                        self.optionsSubList.append(self.database.recordsMenuItemSub[y].getFoodType())
                        print(self.optionsSubList[len(self.optionsSubList) -1])
                
                #With all five options x-pos was 630
                if (len(self.optionsSubList) == 0):
                    tk.messagebox.showinfo("Error", "Issue Connecting to Database. Ending Program Now. " 
                                        + "Please check that all files are correct and try again.")
                    self.mainwindow.destroy()
                    sys.exit(1)
                
                for y in range(len(self.optionsSubList)):
                    
                    '''Choose Button Settings'''

                    #Sub One
                    if (self.optionsSubList[y] == 6):
                        self.btnFoodSubList.append(tk.Radiobutton(self.frameCashierSide, background='#c7d9e1',
                                                    font='{verdana} 14 {}', text='Cupcakes', variable=self.strDessertType,
                                                        value=y, command=lambda: self.buttonPress(5)))
                        self.btnFoodSubList[y].place(anchor='nw', x=615, y=self.yPosBtn)

                    #Sub Two
                    else:
                        self.btnFoodSubList.append(tk.Radiobutton(self.frameCashierSide, background='#c7d9e1',
                                                    font='{verdana} 14 {}', text='Cookies', variable=self.strDessertType,
                                                        value=y, command=lambda: self.buttonPress(6)))
                        self.btnFoodSubList[y].place(anchor='nw', x=615, y=self.yPosBtn)
                        
                    self.yPosBtn = self.yPosBtn + 30

            '''Food Option Buttons'''

            self.btnFoodOptionList = []

            self.xPosBtn = 390
            self.yPosBtn = 260
            
            for z in range(6):
                
                #Checks index to shift to row two
                if (z == 3):
                    self.xPosBtn = 390
                    self.yPosBtn = 340
                self.btnFoodOptionList.append(tk.Button(self.frameCashierSide, font='{verdana} 12 {}', justify='left',
                                        text=("Option " + str(z+1)), wraplength='175'))
                self.btnFoodOptionList[z].place(anchor='nw', height='55', width='180', x=self.xPosBtn, y=self.yPosBtn)
                
                self.xPosBtn = self.xPosBtn + 210

            '''Ticket and Order Alteration Buttons'''
            
            #Resets Data On Ticket
            self.btnReset = tk.Button(self.frameCashierSide, font='{Verdana} 18 {}', text='Clear', command=self.reset)
            self.btnReset.place(anchor='nw', height='55', width='75', x='415', y='565')

            #Add Item to Ticket
            self.btnAdd = tk.Button(self.frameCashierSide, font='{Verdana} 18 {}', text='Add', command=self.addPressed)
            self.btnAdd.place(anchor='nw', height='55', width='125', x='575', y='565')

            #Push Order to Kitchen
            self.btnSubmit = tk.Button(self.frameCashierSide, font='{Verdana} 18 {}', text='Submit', command=self.submitPressed)
            self.btnSubmit.place(anchor='nw', height='55', width='175', x='775', y='565')
            
            #Place Frame
            self.frameCashierSide.pack()

            #Start UI
            self.mainwindow.mainloop()

            #Disconnect from Database
            print(self.database.disconnecting())
    
    def setSeat(self, seat):
        self.currentSeat = seat
        
    def buttonPress(self, val):
        print("Value Selected: " + str(val))
        self.currentItem = ""

        for a in range(len(self.btnFoodOptionList)):
            self.btnFoodOptionList[a].configure(state='normal', bg='white')

        print(self.database.getRecordsMenuItemsSelect(self.database.getCurrentRType(), val))
        
        for b in range(len(self.btnFoodOptionList)):

                if (b < len(self.database.recordsMenuItemSelect)):

                    if (self.database.recordsMenuItemSelect[b].getFoodType() < 5):

                        self.btnFoodOptionList[b].configure(text=self.database.recordsMenuItemSelect[b].getTicketName(), 
                                                        command=lambda i=b: self.buttons(i, self.database.recordsMenuItemSelect[i]), 
                                                        bg='white')
                    else:

                        self.btnFoodOptionList[b].configure(text=self.database.recordsMenuItemSelect[b].getItemName(), 
                                                        command=lambda i=b: self.buttons(i, self.database.recordsMenuItemSelect[i]), 
                                                        bg='white')
                else:
                    self.btnFoodOptionList[b].configure(text="", state='disabled', bg='lightgray')
            
    def buttons(self, index, current):

        #Colors do not work on Mac, will work on pi when shifted over
        
        for b in range(len(self.btnFoodOptionList)):
            if (b == index):

                #Purple-> #CD6BB3
                #Green-> #6BCD85
                self.btnFoodOptionList[b].configure(bg='#6BCD85')
                self.currentItem = current
            else:
                if(b < len(self.database.recordsMenuItemSelect)):
                    self.btnFoodOptionList[b].configure(bg='white')
                else:
                    self.btnFoodOptionList[b].configure(bg='lightgrey')

    def addPressed(self):

        #Getting indexes through loops, Lambdas
        index = self.findIndex(0)

        word = self.currentText("")

        #Dealing with comments
        strShow = ""
        
        if ((not (self.strSeat.get() == "") and not (self.txtCustomer.get() == ""))):

            if (not self.inProgress):

                if ((self.txtTable.get() == "") or (not self.txtTable.get().isdigit())):
                    self.currentTable = 0
                else:
                    self.currentTable = int(self.txtTable.get())

                self.clearHeaderTags.append(self.canvasTicket.create_text(20, 105, anchor='w', tags="order",
                                        text=("Customer: " + self.txtCustomer.get()), fill="black", font=('Helvetica 16')))
                self.clearHeaderTags.append(self.canvasTicket.create_text(225, 65, anchor='w',
                                        text=("Table " + str(self.currentTable)), fill="black", font=('Helvetica 16')))
                self.inProgress = True
            
            if (not self.currentItem == ""):

                decimal.getcontext().prec = 100
                if (not self.txtComments.get(1.0, "end") == "\n"):
                    
                    strShow = (self.currentItem.getTicketName() + " "
                               + (self.txtComments.get(1.0, "end"))[0:(len(self.txtComments.get(1.0, "end"))-1)])
                else:
                    strShow = self.currentItem.getTicketName()

                item = Items(0,self.currentOrder,self.currentTable,self.currentSeat,
                                self.currentItem.getItemName(),self.txtComments.get(1.0, "end"), 
                                self.currentItem.getLingoName(), self.currentItem.getFoodType(), 
                                4)
                item.price = self.currentItem.getItemPrice()
                
                #Tests list length to see if it has anything in it
                if (len(self.listItems) > 0):

                    contains = False
                    self.setDuplicateIndex = 0

                    for x in range(len(self.listItems)): 
                        
                        #Checks for Duplicates, gets values ready for replacement
                        if ((item.getFoodType() == self.listItems[x].getFoodType()) and (
                            item.getSeatNum() == self.listItems[x].getSeatNum())):

                            self.totalCost -= self.listItems[x].price
                            self.lblTotal.config(text=("Total: $" + str(self.totalCost)))
                            contains = True

                            self.duplicateIndex = index(x)
                            print(self.duplicateIndex)
                    
                    #Replace item
                    if (contains):

                        #Replaces Item Data
                        self.listItems[self.duplicateIndex] = item
                        self.ticketList[self.duplicateIndex] = [word(strShow), index(item.price)]
                        self.totalCost += self.currentItem.getItemPrice()
                        self.lblTotal.config(text=("Total: $" + str(self.totalCost)))
                        print("List Item Replaced")

                        #Replaces Visuals on Canvas
                        self.canvasTicket.delete(self.clearFoodTags[self.duplicateIndex][0])
                        self.canvasTicket.delete(self.clearFoodTags[self.duplicateIndex][1])
                        self.clearFoodTags[self.duplicateIndex] = [self.canvasTicket.create_text(20, (self.tagYPos[self.duplicateIndex]), anchor="w",
                                                text=strShow, fill="black", font=('Helvetica 14')),
                                                self.canvasTicket.create_text(300, (self.tagYPos[self.duplicateIndex] + 30), anchor="w",
                                                text=self.currentItem.getItemPrice(), fill="black", font=('Helvetica 14'))]
                    
                    #Add Item
                    else:

                        self.ticketList.append([word(strShow), index(item.price)])
                        self.listItems.append(item)

                        self.totalCost += self.currentItem.getItemPrice()
                        self.lblTotal.config(text=("Total: $" + str(self.totalCost)))
                        print("List Item Added")

                        #Display Item On Ticket
                        self.tagYPos.append(index(self.posY))
                        self.clearFoodTags.append([self.canvasTicket.create_text(20, self.posY, anchor="w",
                                                text=strShow, fill="black", font=('Helvetica 14')),
                                                self.canvasTicket.create_text(300, (self.posY + 30), anchor="w",
                                                text=self.currentItem.getItemPrice(), fill="black", font=('Helvetica 14'))])
                        self.posY = self.posY + 60

                #Add Item
                else:

                    self.ticketList.append([word(strShow), index(item.price)])

                    #Add Item
                    self.listItems.append(item)
                    self.listItems[len(self.listItems)-1].price = self.currentItem.getItemPrice()
                    self.totalCost = decimal.Decimal(self.totalCost) + decimal.Decimal(self.currentItem.getItemPrice())
                    self.lblTotal.config(text=("Total: $" + str(self.totalCost)))
                    print("List Item Added")

                    #Display Item On Ticket
                    self.tagYPos.append(index(self.posY))
                    self.clearFoodTags.append([self.canvasTicket.create_text(20, self.posY, anchor="w",
                                            text=strShow, fill="black", font=('Helvetica 14')),
                                            self.canvasTicket.create_text(300, (self.posY + 30), anchor="w",
                                            text=self.currentItem.getItemPrice(), fill="black", font=('Helvetica 14'))])
                    self.posY = self.posY + 60

                self.txtComments.delete(1.0, "end")
            
            else:
                tk.messagebox.showinfo("Error", "No item selected. Please select an item and try again.")

        else:
            tk.messagebox.showinfo("Error", "No seat and/or Customer name set. "
                                    +"Please fill all required fields and try again.")

    def reset(self):

        if ((len(self.clearFoodTags) > 0) and (len(self.clearHeaderTags) > 0)):

            #Clear canvas, order items
            for item in range(len(self.clearFoodTags)):

                self.canvasTicket.delete(self.clearFoodTags[item][0])
                self.canvasTicket.delete(self.clearFoodTags[item][1])

            #Clear canvas, header items
            for text in range(len(self.clearHeaderTags)):
                self.canvasTicket.delete(self.clearHeaderTags[text])
                    
            
            #Deselect all Radio Buttons
            for a in self.btnFoodList:
                a.deselect()
            
            for b in self.btnFoodSubList:
                b.deselect()
            
            self.btnSOne.deselect()
            self.btnSTwo.deselect()
            self.btnSThree.deselect()
            self.btnSFour.deselect()

            #Clear the Option Button Actions
            for c in self.btnFoodOptionList:
                c.configure(state='normal')
                c.config(bg="white", text="", command=self.filler)

            self.txtComments.delete(1.0, "end")
            self.txtCustomer.delete(0, tk.END)
            self.txtTable.delete(0, tk.END)

            #Cler total
            self.totalCost = 0
            self.lblTotal.configure(text='Total: $0')

            #Clearing lists
            self.clearHeaderTags = list()
            self.clearFoodTags = list()
            self.tagYPos = list()

            #reset order list
            self.listItems = list()

            self.ticketList = list()

            #reset canvas items y-pos
            self.posY = 167

            #Progress halted, boolean reset
            self.inProgress = False

    def submitPressed(self):

        if(len(self.listItems) > 0):

            #User confirmation of deletion
            self.deleteConfirmation = tk.messagebox.askquestion('Submit?',
                            ("Submit $" + str(self.totalCost) + " Order?"),icon = 'warning')

            if self.deleteConfirmation == 'yes':

                #Inserting Item

                
                os.system("sudo chmod 666 /dev/usb/lp0")
                os.system("echo '\t\t\t" + self.database.getCurrentRName() + "'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo '" + self.cashierText + "        Customer: '" + self.txtCustomer.get()+ " >/dev/usb/lp0")
                os.system("echo 'Order: " + str(self.currentOrder) + "        Table: '" + str(self.currentTable) + " >/dev/usb/lp0")
                os.system("echo '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'>/dev/usb/lp0")
                for e in range(0,len(self.listItems)):
                    print(self.listItems[e].getLingoName())
                    self.database.insertRecordItm = [self.currentOrder, self.currentTable, 
                                                    self.listItems[e].getSeatNum(), self.listItems[e].getItemName(),
                                                    self.listItems[e].getComments(), self.listItems[e].getLingoName(),
                                                    self.listItems[e].getFoodType(), 4]
                    self.database.createRecordsItm()

                    os.system("echo '" + self.ticketList[e][0] + "'>/dev/usb/lp0")
                    os.system("echo '\t\t\t\t\t\t" + str(self.ticketList[e][1]) + "'>/dev/usb/lp0")
                    
                #Create Order Record
                self.database.insertRecordOrder = [int(self.currentOrder), int(self.currentTable), 4, float(self.totalCost)]

                '''***Had to cast all variable values for orders else it would not write to table'''
                print(self.database.createRecordsOrder())

                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo 'Total: $" + str(self.totalCost) + "'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo '      ___________________________________'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'>/dev/usb/lp0")
                os.system("echo 'Thank you for your patronage!'>/dev/usb/lp0")
                os.system("echo 'Your Lucky Numbers:'>/dev/usb/lp0")

                collected = False
                luckyList = []
                val = self.findIndex(0)
                luckyString = ""
                
                while not collected:
                    rand = random.randint(0,60)
                    if (rand not in luckyList):
                        luckyList.append(val(rand))
                        luckyString = luckyString + str(val(rand)) + "  "
                    if (len(luckyList) == 7):
                        collected = True
                        
                os.system("echo '" + luckyString + "'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo 'Powered by JCHS Computer Science (Nerds FTW)'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo '\t\tCustomer Copy'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo '\x1d\x56\x01' > /dev/usb/lp0")


                os.system("echo '\t\t\t" + self.database.getCurrentRName() + "'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo '" + self.cashierText + "        Customer: '" + self.txtCustomer.get()+ " >/dev/usb/lp0")
                os.system("echo 'Order: " + str(self.currentOrder) + "        Table: '" + str(self.currentTable) + " >/dev/usb/lp0")
                os.system("echo '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'>/dev/usb/lp0")
                for e in range(0, len(self.listItems)):
                    
                    os.system("echo '" + self.ticketList[e][0] + "'>/dev/usb/lp0")
                    os.system("echo '\t\t\t\t\t\t" + str(self.ticketList[e][1]) + "'>/dev/usb/lp0")
                    
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo 'Total: $" + str(self.totalCost) + "'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo '      ___________________________________'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo 'Powered by JCHS Computer Science (Nerds FTW)'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo '\t\tMerchant Copy'>/dev/usb/lp0")
                os.system("echo ' '>/dev/usb/lp0")
                os.system("echo '\x1d\x56\x01' > /dev/usb/lp0")

                self.reset()

                #Increment Order Number
                self.currentOrder += 1
        else:
            tk.messagebox.showinfo("Error", "No items in order. Add orders and try again")

    #Filler method when buttons clear, avoid unwanted actions after reset
    def filler(self):
        pass
    
    #Lambda function used to get the index value, expecially when 
    #looping through for adding items to the list
    def findIndex(self, current):
        return lambda i: i + current

    def currentText(self, word):
        return lambda text: word + text 
