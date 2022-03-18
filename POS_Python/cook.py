import tkinter as tk
from tkinter import RIGHT, ttk
from tkinter import messagebox
from array import *

class CookApp:
    def __init__(self, conn):

        self.database = conn

        self.stat = [[]]

        #Status for each seat
        self.seatOneState = 0
        self.seatTwoState = 0
        self.seatThreeState = 0
        self.seatFourState = 0
        
        #Holds Frames, Order Contents
        self.framelblOrder = list()

        #Mark Items Completed, separated by seat number
        self.btnSeatOneDone = list()
        self.btnSeatTwoDone = list()
        self.btnSeatThreeDone = list()
        self.btnSeatFourDone = list()

        #Mark Items In Progress, separated by seat number
        self.btnSeatOneProgress = list()
        self.btnSeatTwoProgress = list()
        self.btnSeatThreeProgress = list()
        self.btnSeatFourProgress = list()

        #Mark Items In Progress, separated by seat number
        self.btnSeatOneDelete = list()
        self.btnSeatTwoDelete = list()
        self.btnSeatThreeDelete = list()
        self.btnSeatFourDelete = list()

        #Display Order Text Boxes, separated by seat number
        self.txtSeatOne = list()
        self.txtSeatTwo = list()
        self.txtSeatThree = list()
        self.txtSeatFour = list()

        #Root, Main Window
        self.mainwindow = tk.Tk()
        self.mainwindow.title("Cook")

        '''Header Frame Config and Components'''

        #Title Frame, holds header lbl and refresh button
        self.frameTitle = tk.Frame(self.mainwindow, width=800, heigh=70, bg='#c7d9e1')
        self.frameTitle.pack(side='top')

        #Header 
        self.lblHeader = tk.Label(self.frameTitle, text='Orders', font='{Verdana} 22 {bold}', bg="#c7d9e1")
        self.lblHeader.place(anchor='nw', width='120', x='355', y='8')

        #Refresh Record Data Trigger
        self.btnReload = tk.Button(self.frameTitle, text='Reload', font='{Verdana} 15 {}', command=self.refreshView)
        self.btnReload.place(anchor='nw', height='50', width='120', x='595', y='10')

        #Labels describing what colors mean on UI txt fields
        self.lblKeyPending = tk.Label(self.frameTitle, text='Not Started', font='{Verdana} 11 {bold}', bg='white', width=10,
                                      highlightthickness=1, highlightbackground='black')
        self.lblKeyPending.place(x=5, y=5)
        self.lblKeyProgress = tk.Label(self.frameTitle, text='In Progress', font='{Verdana} 11 {bold}', bg="yellow", width=10,
                                       highlightthickness=1, highlightbackground='black')
        self.lblKeyProgress.place(x=125, y=5)
        self.lblKeyDone = tk.Label(self.frameTitle, text='Done', font='{Verdana} 11 {bold}', bg="#a4ecbf", width=10,
                                   highlightthickness=1, highlightbackground='black')
        self.lblKeyDone.place(x=5, y=37)
        self.lblKeyCanceled = tk.Label(self.frameTitle, text='Canceled', font='{Verdana} 11 {bold}', bg="#f0a09a", width=10,
                                       highlightthickness=1, highlightbackground='black')
        self.lblKeyCanceled.place(x=125, y=37)

        '''Scrolling Frame DIY Config'''

        #Frame containing scroll items
        self.frameContainer = ttk.Frame(self.mainwindow)

        #Canvases are the only component that can use scrolling
        self.canvas = tk.Canvas(self.frameContainer, height=335, width=785, bg='#c7d9e1')

        self.ordersScroll = ttk.Scrollbar(self.frameContainer, orient="vertical", command=self.canvas.yview)

        self.mainFrame = ttk.Frame(self.canvas, style='TFrame')

        self.mainFrame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.mainFrame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.ordersScroll.set)

        self.imgProgressBtn= tk.PhotoImage(file='imgProgress.gif')
        self.imgDoneBtn= tk.PhotoImage(file='imgDone.gif')
        self.imgDeleteBtn= tk.PhotoImage(file='imgDelete.gif')

        #Placing scrolling frame components
        self.frameContainer.pack(side='bottom')
        self.canvas.pack(side="left", fill="both", expand=True)
        self.ordersScroll.pack(side="right", fill="y")

        #Trigger Automatic Refresh Start
        self.frameContainer.after(2000, self.test)
        self.count = 0

        #Run UI
        self.mainwindow.mainloop()
        
    def test(self):
        print("hello, world " + str(self.count))
        self.count = self.count + 1
        self.frameContainer.after(2000, self.test)
        
        ordersToShow = self.database.getNewOrderShow()
        
        if (len(ordersToShow) >= 1):
            firstNewOrder = ordersToShow[0]
            lastOrder = ordersToShow[-1]
            while ((len(self.framelblOrder)-1) < lastOrder):
                self.framelblOrder.append(0)
                
            while ((len(self.stat)-1) < lastOrder):
                self.stat.append(0)
                
            while ((len(self.txtSeatOne)-1) < lastOrder):
                self.txtSeatOne.append(0)
                
            while ((len(self.txtSeatTwo)-1) < lastOrder):
                self.txtSeatTwo.append(0)
                
            while ((len(self.txtSeatThree)-1) < lastOrder):
                self.txtSeatThree.append(0)
                
            while ((len(self.txtSeatFour)-1) < lastOrder):
                self.txtSeatFour.append(0)
                
            while ((len(self.btnSeatOneProgress)-1) < lastOrder):
                self.btnSeatOneProgress.append(0)
                
            while ((len(self.btnSeatOneDone)-1) < lastOrder):
                self.btnSeatOneDone.append(0)
                
            while ((len(self.btnSeatOneDelete)-1) < lastOrder):
                self.btnSeatOneDelete.append(0)
                
            while ((len(self.btnSeatTwoProgress)-1) < lastOrder):
                self.btnSeatTwoProgress.append(0)
                
            while ((len(self.btnSeatTwoDone)-1) < lastOrder):
                self.btnSeatTwoDone.append(0)
                
            while ((len(self.btnSeatTwoDelete)-1) < lastOrder):
                self.btnSeatTwoDelete.append(0)
                
            while ((len(self.btnSeatThreeProgress)-1) < lastOrder):
                self.btnSeatThreeProgress.append(0)
                
            while ((len(self.btnSeatThreeDone)-1) < lastOrder):
                self.btnSeatThreeDone.append(0)
                
            while ((len(self.btnSeatThreeDelete)-1) < lastOrder):
                self.btnSeatThreeDelete.append(0)
                
            while ((len(self.btnSeatFourProgress)-1) < lastOrder):
                self.btnSeatFourProgress.append(0)
                
            while ((len(self.btnSeatFourDone)-1) < lastOrder):
                self.btnSeatFourDone.append(0)
                
            while ((len(self.btnSeatFourDelete)-1) < lastOrder):
                self.btnSeatFourDelete.append(0)
                
            print("num orders to show: " + str(len(ordersToShow)))
            for x in ordersToShow:
                #Adding Label Frames to config components to

                orderNumber = int(x)

                self.stat[orderNumber] = [0, 0, 0, 0]                


                seatOne = self.database.getLingoNames(orderNumber, 1)
                if((len(seatOne)) == 0):
                    self.stat[orderNumber][0] = 2
                seatTwo = self.database.getLingoNames(orderNumber, 2)
                if((len(seatTwo)) == 0):
                    self.stat[orderNumber][1] = 2
                seatThree = self.database.getLingoNames(orderNumber, 3)
                if((len(seatThree)) == 0):
                    self.stat[orderNumber][2] = 2
                seatFour = self.database.getLingoNames(orderNumber, 4)
                if((len(seatFour)) == 0):
                    self.stat[orderNumber][3] = 2
                table = self.database.getTableNum(orderNumber)

                self.framelblOrder[orderNumber] = (tk.LabelFrame(self.mainFrame, text= ('Order Number: ' + str(orderNumber) 
                                                + '\t' + ' Table ' + str(table)), font='{Verdana} 18 {bold}', 
                                                bg='lightgray', height=430, width=750))
                    
                print("first order to show: " + str(firstNewOrder))
                print("number of the order processing: " + str(orderNumber))
                print("number of frame labels: " + str(len(self.framelblOrder)))
                print("number of orders in the 2d list: " + str(len(self.stat)))
                '''Seat One Components'''

                #Label Indicating Seat One
                self.lblSeat1 = tk.Label(self.framelblOrder[orderNumber], text='Seat 1', font='{Verdana} 14 {bold}', bg='lightgray')
                self.lblSeat1.place(anchor='nw', x='10', y='30')

                #Text Box Displaying Seat One Order Items
                self.txtSeatOne[orderNumber] = tk.Text(self.framelblOrder[orderNumber], height='10', font='{Verdana} 12 {}')
                self.txtSeatOne[orderNumber].insert(1.0, seatOne)
                self.txtSeatOne[orderNumber].configure(state='disabled')
                self.txtSeatOne[orderNumber].place(anchor='nw', height='55', width='350', x='100', y='30')

                #Set Item to In Progress
                self.btnSeatOneProgress[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgProgressBtn, 
                                                font='{Verdana} 14 {}', command= lambda num=orderNumber: self.inProgressBtnFunc(1, num))
                self.btnSeatOneProgress[orderNumber].place(anchor='nw', height='55', width='55', x='480', y='30')

                #Complete Item
                self.btnSeatOneDone[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgDoneBtn, 
                                                font='{Verdana} 14 {}', command= lambda num=orderNumber: self.doneBtnFunc(1, num))
                self.btnSeatOneDone[orderNumber].place(anchor='nw', height='55', width='55', x='575', y='30')

                #Cancel Item
                self.btnSeatOneDelete[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgDeleteBtn, 
                                                font='{Verdana} 14 {}', command= lambda num=orderNumber: self.cancelBtnFunc(1, num))
                self.btnSeatOneDelete[orderNumber].place(anchor='nw', height='55', width='55', x='670', y='30')

                '''Seat Two Components'''

                #Label Indicating Seat Two
                self.lblSeat2 = tk.Label(self.framelblOrder[orderNumber], text='Seat 2', font='{Verdana} 14 {bold}', bg='lightgray')
                self.lblSeat2.place(anchor='nw', x='10', y='120')

                #Text Box Displaying Seat Two Order Items
                self.txtSeatTwo[orderNumber] = tk.Text(self.framelblOrder[orderNumber], height='10', font='{Verdana} 14 {}')
                self.txtSeatTwo[orderNumber].insert(1.0, seatTwo)
                self.txtSeatTwo[orderNumber].configure(state='disabled')
                self.txtSeatTwo[orderNumber].place(anchor='nw', height='55', width='350', x='100', y='120')

                #Set Item to In Progress
                self.btnSeatTwoProgress[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgProgressBtn, 
                                                    font='{Verdana} 14 {}', command= lambda num=orderNumber: self.inProgressBtnFunc(2, num))
                self.btnSeatTwoProgress[orderNumber].place(anchor='nw', height='55', width='55', x='480', y='120')

                #Complete Item
                self.btnSeatTwoDone[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgDoneBtn, 
                                                font='{Verdana} 14 {}', command= lambda num=orderNumber: self.doneBtnFunc(2, num))
                self.btnSeatTwoDone[orderNumber].place(anchor='nw', height='55', width='55', x='575', y='120')

                #Cancel Item
                self.btnSeatTwoDelete[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgDeleteBtn,  
                                                font='{Verdana} 14 {}', command= lambda num=orderNumber: self.cancelBtnFunc(2, num))
                self.btnSeatTwoDelete[orderNumber].place(anchor='nw', height='55', width='55', x='670', y='120')

                '''Seat Three Components'''

                #Label Indicating Seat Three
                self.lblSeat3 = tk.Label(self.framelblOrder[orderNumber], text='Seat 3', font='{Verdana} 14 {bold}', bg='lightgray')
                self.lblSeat3.place(anchor='nw', x='10', y='210')

                #Text Box Displaying Seat Three Order Items
                self.txtSeatThree[orderNumber] = tk.Text(self.framelblOrder[orderNumber], height='10', font='{Verdana} 14 {}')
                self.txtSeatThree[orderNumber].insert(1.0, seatThree)
                self.txtSeatThree[orderNumber].configure(state='disabled')
                self.txtSeatThree[orderNumber].place(anchor='nw', height='55', width='350', x='100', y='210')

                #Set Item to In Progress
                self.btnSeatThreeProgress[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgProgressBtn, 
                                                    font='{Verdana} 14 {}', command= lambda num=orderNumber: self.inProgressBtnFunc(3, num))
                self.btnSeatThreeProgress[orderNumber].place(anchor='nw', height='55', width='55', x='480', y='210')

                #Complete Item
                self.btnSeatThreeDone[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgDoneBtn, 
                                                font='{Verdana} 14 {}', command= lambda num=orderNumber: self.doneBtnFunc(3, num))
                self.btnSeatThreeDone[orderNumber].place(anchor='nw', height='55', width='55', x='575', y='210')

                #Cancel Item
                self.btnSeatThreeDelete[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgDeleteBtn,  
                                                    font='{Verdana} 14 {}', command= lambda num=orderNumber: self.cancelBtnFunc(3, num))
                self.btnSeatThreeDelete[orderNumber].place(anchor='nw', height='55', width='55', x='670', y='210')

                '''Seat Four Components'''

                #Label Indicating Seat Four
                self.lblSeat4 = tk.Label(self.framelblOrder[orderNumber], text='Seat 4', font='{Verdana} 14 {bold}', bg='lightgray')
                self.lblSeat4.place(anchor='nw', x='10', y='300')

                #Text Box Displaying Seat Four Order Items
                self.txtSeatFour[orderNumber] = tk.Text(self.framelblOrder[orderNumber], height='10', font='{Verdana} 14 {}')
                self.txtSeatFour[orderNumber].insert(1.0, seatFour)
                self.txtSeatFour[orderNumber].configure(state='disabled')
                self.txtSeatFour[orderNumber].place(anchor='nw', height='55', width='350', x='100', y='300')

                #Set Item to In Progress
                self.btnSeatFourProgress[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgProgressBtn, 
                                                    font='{Verdana} 14 {}', command= lambda num=orderNumber: self.inProgressBtnFunc(4, num))
                self.btnSeatFourProgress[orderNumber].place(anchor='nw', height='55', width='55', x='480', y='300')
                        
                #Complete Item
                self.btnSeatFourDone[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgDoneBtn,
                                                font='{Verdana} 14 {}', command= lambda num=orderNumber: self.doneBtnFunc(4, num))
                self.btnSeatFourDone[orderNumber].place(anchor='nw', height='55', width='55', x='575', y='300')

                #Cancel Item
                self.btnSeatFourDelete[orderNumber] = tk.Button(self.framelblOrder[orderNumber], image=self.imgDeleteBtn,  
                                                    font='{Verdana} 14 {}', command= lambda num=orderNumber: self.cancelBtnFunc(4, num))
                self.btnSeatFourDelete[orderNumber].place(anchor='nw', height='55', width='55', x='670', y='300')

                #place Label Frame
                self.framelblOrder[orderNumber].pack(padx=(20, 55),pady=20)
                #, padx=(55, 15)

                self.database.updateStatusOrder(orderNumber, 0)
                self.database.updateStatusItem(orderNumber, 1, 0)
                self.database.updateStatusItem(orderNumber, 2, 0)
                self.database.updateStatusItem(orderNumber, 3, 0)
                self.database.updateStatusItem(orderNumber, 4, 0)

            

    def itemStatusShift(self, seat, index, status):

        '''Color key:
        In Progress: #fcf9c1
        Done: #a4ecbf
        Canceled:#f0a09a'''

        #Checks Seat Number
        if (seat == 1):

            #Check Status to determine color and updates
            if(status == 1):
                self.seatOneState = 1
                self.txtSeatOne[index].config(bg='#fcf9c1')
                print("one")
                #update order status query call
            elif (status == 2):
                self.seatOneState = 2
                self.txtSeatOne[index].config(bg='#a4ecbf')
                print("two")
                #update order status query call
            else:
                self.seatOneState = 3
                self.txtSeatOne[index].config(bg='#f0a09a')
                print("three")
                #update order status query call

        elif (seat == 2):

            #Check Status to determine color and updates
            if(status == 1):
                self.seatTwoState = 1
                self.txtSeatTwo[index].config(bg='#fcf9c1')
                #update order status query call
            elif (status == 2):
                self.seatTwoState = 2
                self.txtSeatTwo[index].config(bg='#a4ecbf')
                #update order status query call
            else:
                self.seatTwoState = 3
                self.txtSeatTwo[index].config(bg='#f0a09a')
                #update order status query call

        elif (seat == 3):

            #Check Status to determine color and updates
            if(status == 1):
                self.seatThreeState = 1
                self.txtSeatThree[index].config(bg='#fcf9c1')
                #update order status query call
            elif (status == 2):
                self.seatThreeState = 2
                self.txtSeatThree[index].config(bg='#a4ecbf')
                #update order status query call
            else:
                self.seatThreeState = 3
                self.txtSeatThree[index].config(bg='#f0a09a')
                #update order status query call
        else:

            #Check Status to determine color and updates
            if(status == 1):
                self.seatFourState = 1
                self.txtSeatFour[index].config(bg='#fcf9c1')
                #update order status query call
            elif (status == 2):
                self.seatFourState = 2
                self.txtSeatFour[index].config(bg='#a4ecbf')
                #update order status query call
            else:
                self.seatFourState = 3
                self.txtSeatFour[index].config(bg='#f0a09a')
                #update order status query call


    def refreshView(self):
        print("Refresh pressed")
        self.txtSeatOne[0].config(state='normal')
        self.txtSeatOne[0].delete(1.0,"end")
        self.txtSeatOne[0].insert(1.0, "New text")
        self.txtSeatOne[0].config(state='disabled')

    def alertBoxDone(self):
        return messagebox.askquestion("Validation", "Are you sure that you want to clear this order?")

    def alertBoxCancel(self):
        return messagebox.askquestion("Validation", "Are you sure that you want to cancel this order?")

    def doneBtnFunc(self, seat, orderNumber):
        if(self.alertBoxDone()):
            self.itemStatusShift(seat, orderNumber, 2)
            self.stat[orderNumber][seat - 1] = 2
            self.database.updateStatusItem(orderNumber, seat, 2)
            if(self.checkStatus(orderNumber) == 2):
                self.database.updateStatusOrder(orderNumber, 2)
                self.framelblOrder[orderNumber].destroy()
            elif(self.orderCompleted(orderNumber)):
                self.database.updateStatusOrder(orderNumber, 2)
                self.framelblOrder[orderNumber].destroy()

    def cancelBtnFunc(self, seat, orderNumber):
        if(self.alertBoxCancel()):
            self.itemStatusShift(seat, orderNumber, 3)
            self.stat[orderNumber][seat - 1] = 3
            self.database.updateStatusItem(orderNumber, seat, 3)
            if(self.checkStatus(orderNumber) == 3):
                self.database.updateStatusOrder(orderNumber, 3)
                self.framelblOrder[orderNumber].destroy()
            elif(self.orderCompleted(orderNumber)):
                self.database.updateStatusOrder(orderNumber, 2)
                self.framelblOrder[orderNumber].destroy()

    def inProgressBtnFunc(self, seat, orderNumber):
        self.itemStatusShift(seat, orderNumber, 1)
        self.stat[orderNumber][seat - 1] = 1
        self.database.updateStatusItem(orderNumber, seat, 1)
        if(self.checkStatus(orderNumber) == 1):
            self.database.updateStatusOrder(orderNumber, 1)
        elif(self.orderCompleted(orderNumber)):
                self.database.updateStatusOrder(orderNumber, 2)
                self.framelblOrder[orderNumber].destroy()
             
    def checkStatus(self, orderNum):
        status = self.stat[orderNum][0]
        for x in self.stat[orderNum]:
            if(status != x):
                return 9
        return status
    
    def orderCompleted(self, orderNum):
        for x in self.stat[orderNum]:
            if(not((x == 2) or (x == 3))):
                return False
            
        return True
    



