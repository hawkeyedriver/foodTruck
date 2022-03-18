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

        '''Header Frame Config and Components'''

        #Title Frame, holds header lbl and refresh button
        self.frameTitle = tk.Frame(self.mainwindow, width=970, heigh=70, bg='#c7d9e1')
        self.frameTitle.pack(side='top')

        #Header 
        self.lblHeader = tk.Label(self.frameTitle, text='Orders', font='{Verdana} 22 {bold}', bg="#c7d9e1")
        self.lblHeader.place(anchor='nw', width='90', x='440', y='8')

        #Refresh Record Data Trigger
        self.btnReload = tk.Button(self.frameTitle, text='Reload', font='{Verdana} 15 {}', command=self.refreshView)
        self.btnReload.place(anchor='nw', height='30', width='90', x='750', y='10')

        #Labels describing what colors mean on UI txt fields
        self.lblKeyPending = tk.Label(self.frameTitle, text='Not Started', font='{Verdana} 14 {bold}')
        self.lblKeyPending.place(x=5, y=5)
        self.lblKeyProgress = tk.Label(self.frameTitle, text='In Progress', font='{Verdana} 14 {bold}', bg="#fcf9c1")
        self.lblKeyProgress.place(x=125, y=5)
        self.lblKeyDone = tk.Label(self.frameTitle, text='Done', font='{Verdana} 14 {bold}', bg="#a4ecbf", width=9)
        self.lblKeyDone.place(x=5, y=37)
        self.lblKeyCanceled = tk.Label(self.frameTitle, text='Canceled', font='{Verdana} 14 {bold}', bg="#f0a09a", width=9)
        self.lblKeyCanceled.place(x=125, y=37)

        '''Scrolling Frame DIY Config'''

        #Frame containing scroll items
        self.frameContainer = ttk.Frame(self.mainwindow)

        #Canvases are the only component that can use scrolling
        self.canvas = tk.Canvas(self.frameContainer, height='600', width='950', bg='#c7d9e1')

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
        firstNewOrder = ordersToShow[0]
        for x in ordersToShow:
            #Adding Label Frames to config components to

            orderNumber = int(x)
            self.stat.insert(orderNumber, [0, 0, 0, 0])

            for orderNumber in range(firstNewOrder, (self.stat.len())):
                seatOne = self.database.getLingoNames(orderNumber, 1)
                seatTwo = self.database.getLingoNames(orderNumber, 2)
                seatThree = self.database.getLingoNames(orderNumber, 3)
                seatFour = self.database.getLingoNames(orderNumber, 4)

                self.framelblOrder.append(tk.LabelFrame(self.mainFrame, text= ('Order Number: ' + orderNumber 
                                                + '\t' + ' Table '), font='{Verdana} 18 {bold}', 
                                                bg='lightgray', height='400', width='850'))

                '''Seat One Components'''

                #Label Indicating Seat One
                self.lblSeat1 = tk.Label(self.framelblOrder[orderNumber], text='Seat 1', font='{Verdana} 14 {bold}', bg='lightgray')
                self.lblSeat1.place(anchor='nw', x='10', y='30')

                #Text Box Displaying Seat One Order Items
                self.txtSeatOne.append(tk.Text(self.framelblOrder[orderNumber], height='10', font='{Verdana} 14 {}', text = seatOne))
                self.txtSeatOne[orderNumber].insert(1.0, "Items")
                self.txtSeatOne[orderNumber].configure(state='disabled')
                self.txtSeatOne[orderNumber].place(anchor='nw', height='55', width='450', x='100', y='30')

                #Set Item to In Progress
                self.btnSeatOneProgress.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgProgressBtn, 
                                                font='{Verdana} 14 {}', command=self.inProgressBtnFunc(1, orderNumber)))
                self.btnSeatOneProgress[orderNumber].place(anchor='nw', height='55', width='55', x='580', y='30')

                #Complete Item
                self.btnSeatOneDone.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgDoneBtn, 
                                            font='{Verdana} 14 {}', command=self.doneBtnFunc(1, orderNumber)))
                self.btnSeatOneDone[orderNumber].place(anchor='nw', height='55', width='55', x='665', y='30')

                #Cancel Item
                self.btnSeatOneDelete.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgDeleteBtn, 
                                            font='{Verdana} 14 {}', command=self.cancelBtnFunc(1, orderNumber)))
                self.btnSeatOneDelete[orderNumber].place(anchor='nw', height='55', width='55', x='750', y='30')

                '''Seat Two Components'''

                #Label Indicating Seat Two
                self.lblSeat2 = tk.Label(self.framelblOrder[orderNumber], text='Seat 2', font='{Verdana} 14 {bold}', bg='lightgray')
                self.lblSeat2.place(anchor='nw', x='10', y='120')

                #Text Box Displaying Seat Two Order Items
                self.txtSeatTwo.append(tk.Text(self.framelblOrder[orderNumber], height='10', font='{Verdana} 14 {}', text = seatTwo))
                self.txtSeatTwo[orderNumber].insert(1.0, "Items")
                self.txtSeatTwo[orderNumber].configure(state='disabled')
                self.txtSeatTwo[orderNumber].place(anchor='nw', height='55', width='450', x='100', y='120')

                #Set Item to In Progress
                self.btnSeatTwoProgress.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgProgressBtn, 
                                                font='{Verdana} 14 {}', command=self.inProgressBtnFunc(2, orderNumber)))
                self.btnSeatTwoProgress[orderNumber].place(anchor='nw', height='55', width='55', x='580', y='120')

                #Complete Item
                self.btnSeatTwoDone.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgDoneBtn, 
                                            font='{Verdana} 14 {}', command=self.doneBtnFunc(2, orderNumber)))
                self.btnSeatTwoDone[orderNumber].place(anchor='nw', height='55', width='55', x='665', y='120')

                #Cancel Item
                self.btnSeatTwoDelete.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgDeleteBtn,  
                                            font='{Verdana} 14 {}', command=self.cancelBtnFunc(2, orderNumber)))
                self.btnSeatTwoDelete[orderNumber].place(anchor='nw', height='55', width='55', x='750', y='120')

                '''Seat Three Components'''

                #Label Indicating Seat Three
                self.lblSeat3 = tk.Label(self.framelblOrder[orderNumber], text='Seat 3', font='{Verdana} 14 {bold}', bg='lightgray')
                self.lblSeat3.place(anchor='nw', x='10', y='210')

                #Text Box Displaying Seat Three Order Items
                self.txtSeatThree.append(tk.Text(self.framelblOrder[orderNumber], height='10', font='{Verdana} 14 {}', text = seatThree))
                self.txtSeatThree[orderNumber].insert(1.0, "Items")
                self.txtSeatThree[orderNumber].configure(state='disabled')
                self.txtSeatThree[orderNumber].place(anchor='nw', height='55', width='450', x='100', y='210')

                #Set Item to In Progress
                self.btnSeatThreeProgress.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgProgressBtn, 
                                                font='{Verdana} 14 {}', command=self.inProgressBtnFunc(3, orderNumber)))
                self.btnSeatThreeProgress[orderNumber].place(anchor='nw', height='55', width='55', x='580', y='210')

                #Complete Item
                self.btnSeatThreeDone.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgDoneBtn, 
                                            font='{Verdana} 14 {}', command=self.doneBtnFunc(3, orderNumber)))
                self.btnSeatThreeDone[orderNumber].place(anchor='nw', height='55', width='55', x='665', y='210')

                #Cancel Item
                self.btnSeatThreeDelete.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgDeleteBtn,  
                                                font='{Verdana} 14 {}', command=self.cancelBtnFunc(3, orderNumber)))
                self.btnSeatThreeDelete[orderNumber].place(anchor='nw', height='55', width='55', x='750', y='210')

                '''Seat Four Components'''

                #Label Indicating Seat Four
                self.lblSeat4 = tk.Label(self.framelblOrder[orderNumber], text='Seat 4', font='{Verdana} 14 {bold}', bg='lightgray')
                self.lblSeat4.place(anchor='nw', x='10', y='300')

                #Text Box Displaying Seat Four Order Items
                self.txtSeatFour.append(tk.Text(self.framelblOrder[orderNumber], height='10', font='{Verdana} 14 {}', text = seatFour))
                self.txtSeatFour[orderNumber].insert(1.0, "Items")
                self.txtSeatFour[orderNumber].configure(state='disabled')
                self.txtSeatFour[orderNumber].place(anchor='nw', height='55', width='450', x='100', y='300')

                #Set Item to In Progress
                self.btnSeatFourProgress.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgProgressBtn, 
                                                font='{Verdana} 14 {}', command=self.inProgressBtnFunc(4, orderNumber)))
                self.btnSeatFourProgress[orderNumber].place(anchor='nw', height='55', width='55', x='580', y='300')
                    
                #Complete Item
                self.btnSeatFourDone.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgDoneBtn,
                                            font='{Verdana} 14 {}', command=self.doneBtnFunc(4, orderNumber)))
                self.btnSeatFourDone[orderNumber].place(anchor='nw', height='55', width='55', x='665', y='300')

                #Cancel Item
                self.btnSeatFourDelete.append(tk.Button(self.framelblOrder[orderNumber], image=self.imgDeleteBtn,  
                                                font='{Verdana} 14 {}', command=self.cancelBtnFunc(4, orderNumber)))
                self.btnSeatFourDelete[orderNumber].place(anchor='nw', height='55', width='55', x='750', y='300')

                #place Label Frame
                self.framelblOrder[orderNumber].pack(padx=(60, 60), pady=20)

                self.database.updateStatusOrder(orderNumber, 0)

            

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

    def alertboxDone(self):
        return messagebox.askquestion("Validation", "Are you sure that you want to clear this order?")

    def alertboxCancel(self):
        return messagebox.askquestion("Validation", "Are you sure that you want to cancel this order?")

    def doneBtnFunc(self, seat, orderNumber):
        if(self.alertBoxDone()):
            self.itemStatusShift(seat, orderNumber, 2)
            self.stat[orderNumber][seat - 1] = 2
            self.changeDBStatus(orderNumber)
            self.framelblOrder[orderNumber].destroy()

    def cancelBtnFunc(self, seat, orderNumber):
        if(self.alertBoxCancel()):
            self.itemStatusShift(seat, orderNumber, 3)
            self.stat[orderNumber][seat - 1] = 3
            self.changeDBStatus(orderNumber)
            self.framelblOrder[orderNumber].destroy()

    def inProgressBtnFunc(self, seat, orderNumber):
        self.itemStatusShift(seat, orderNumber, 1)
        self.stat[orderNumber][seat - 1] = 1
        self.changeDBStatus(orderNumber)
             
    def changeDBStatus(self, orderNumber):
        commonStatus = self.checkStatus(orderNumber)
        if (commonStatus != 9):
            self.database.updateStatusOrder(orderNumber, commonStatus)
        seatNum = 0
        for x in self.stat[orderNumber]:
            self.database.updateStatusItem(orderNumber, seatNum, x)
            seatNum += 1

    def checkStatus(self, orderNum):
        status = self.stat[orderNum][0]
        for x in self.stat[orderNum]:
            if(status != x):
                return 9
        return status 

        
