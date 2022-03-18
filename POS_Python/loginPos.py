"""Login Class POS"""
import tkinter as tk
from tkinter import messagebox
from posDB import PosDB

class LoginRestaurantApp:
    
    def __init__(self, db):

        self.database = db
        #self.database.connecting()
        
        if (self.database.connecting() != "Connected"):
            tk.messagebox.showinfo("Error", "Issue Connecting to Database. Ending Program Now. " + 
                                    "Please check that all files are correct and try again.")
        else:
            #Main Window
            self.mainwindow = tk.Tk()
            self.mainwindow.title("Login")

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
                                                            "App that connects to a database and functions"
                                                            +"as the cashier side of a POS system"))

            '''Menu Configs'''

            #Adding all Menu Items to Menu
            self.cashierMenu.add_cascade(label="File", menu=self.fileMenu)
            self.cashierMenu.add_cascade(label="Connection", menu=self.connectionMenu)
            self.cashierMenu.add_cascade(label="Help", menu=self.helpMenu)

            #Configuring Menu to the Window
            self.mainwindow.config(menu=self.cashierMenu)

            #Frame
            self.frame = tk.Frame(self.mainwindow, background='#c7d9e1', height='450', width='800')

            """Components"""

            '''Labels'''

            #Title
            self.lblTitle = tk.Label(self.frame, background='#c7d9e1', font='{verdana} 40 {}', text='Select Your Restaurant')
            self.lblTitle.place(anchor='nw', width='800', x='0', y='15')

            #Restaurant Option Indicator
            self.lblRestaurant = tk.Label(self.frame, background='#c7d9e1', font='{verdana} 26 {}', text='Restaurant: ')
            self.lblRestaurant.place(anchor='nw', x='100', y='140')

            #Cashier Name Indicator
            self.lblCashier = tk.Label(self.frame, background='#c7d9e1', font='{verdana} 26 {}', text='Cashier: ')
            self.lblCashier.place(anchor='nw', x='115', y='250')

            '''Text Fields'''

            #Get Cashier Text Name
            self.txtCashier = tk.Entry(self.frame, font='{verdana} 18 {}')
            self.txtCashier.place(anchor='nw', height='30', width='350', x='380', y='255')

            '''Option Menus (Drop Downs)'''

            self.strRestaurant = tk.StringVar()
            self.strRestaurant.set("Name")

            self.valuesRestaurant = list()

            for x in range(1,len(self.database.recordsRestaurant)):
                self.valuesRestaurant.append(self.database.recordsRestaurant[x].getStoreName())

            #Drop Down of Restaurant Names
            self.optionRestaurant = tk.OptionMenu(self.frame, self.strRestaurant, 
                        self.database.recordsRestaurant[0].getStoreName(), *self.valuesRestaurant)
            self.optionRestaurant.place(anchor='nw', width='350', x='380', y='150')

            '''Buttons'''
            
            #Login 
            self.btnLogin = tk.Button(self.frame, font='{verdana} 16 {}', text='Login', command=self.executeLogin)
            self.btnLogin.place(anchor='nw', height='50', width='100', x='345', y='360')
            
            #Add Frame to Window
            self.frame.pack()

            #Display UI
            self.mainwindow.mainloop()

    #Validates field inputs then close UI if valid
    def executeLogin(self):

        if (not (self.txtCashier.get() == "") and not (self.strRestaurant.get()=="Name")):
            print("Worked")

            #Check for Restaurant Name, set Current Restaurant Type in class object to use for cashier element
            for x in range(len(self.database.recordsRestaurant)):
                if (self.database.recordsRestaurant[x].getStoreName() == self.strRestaurant.get()):    
                    self.database.setCurrentRType(self.database.recordsRestaurant[x].getRestaurantType())
            
            #Set restaurant Name and Cashier Name in class object to use for cashier element, ticket display
            self.database.setCurrentRName(self.strRestaurant.get())
            self.database.setCashierName(self.txtCashier.get())
            self.mainwindow.destroy()
        else:
            tk.messagebox.showinfo("Invalid",
                                    "Please make sure all fields are properly filled out")
