from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import numpy as np
import mysql.connector

class Alert():
    def __init__(self, master,mydb):
        def update(rows):
            self.trv.delete(*self.trv.get_children())
            for i in rows:
                self.trv.insert('','end', values=i)
            
        def vhc_update(rows):
            self.vhctrv.delete(*self.vhctrv.get_children())
            for i in rows:
                self.vhctrv.insert('','end', values=i)
        def driver_alert():
            self.mycursor = mydb.cursor()
            query = "SElECT Driver_ID, Firstname, Phone, PCO_Exp FROM driver Where PCO_Exp <CURDATE() or PCO_Exp<CURDATE()+30"
            self.mycursor.execute(query)
            rows = self.mycursor.fetchall()
            if len(list(rows))>0:
                rows = list(rows[0])
                rows.insert(2,'PCO')
                tablerow=[tuple(list(rows))]
            else:
                tablerow = [tuple(list(rows))]
            query2 = "SElECT Driver_ID, Firstname, Phone, DL_Exp FROM driver Where DL_Exp <CURDATE() or DL_Exp<CURDATE()+30"
            self.mycursor.execute(query2)
            rows2 = self.mycursor.fetchall()
            if len(list(rows2))>0:
                rows2 = list(rows2[0])
                rows2.insert(3,'DL')
                tablerow2=[tuple(list(rows2))]
                tb = tablerow + tablerow2
                update(tb)
            else:
                tablerow2= [tuple(list(rows2))]
                tb = tablerow + tablerow2
                update(tb)
        def Vehicle_alert():
            self.mycursor = mydb.cursor()
            query = "SElECT Reg_No, DriverID, PCO_Exp FROM vehicle Where PCO_Exp <CURDATE() or PCO_Exp<CURDATE()+30"
            self.mycursor.execute(query)
            rows = self.mycursor.fetchall()
            if len(list(rows))>0:
                rows = list(rows[0])

                rows.insert(2,'PCO')
                tablerow=[tuple(list(rows))]
            else:
                tablerow = [tuple(list(rows))]

            
            query2 = "SElECT Reg_No, DriverID, MOT_Exp FROM vehicle Where MOT_Exp <CURDATE() or MOT_Exp<CURDATE()+30"
            self.mycursor.execute(query2)
            rows2 = self.mycursor.fetchall()
            if len(list(rows2))>0:
                tablerow2=[]
                for i in list(rows2):
                    rows2 = list(i)
                    rows2.insert(2,'MOT')
                    tablerow2.append(tuple(rows2))
                tb = tablerow + tablerow2
                vhc_update(tb)
            else:
                tablerow2= [tuple(list(rows2))]
                tb = tablerow + tablerow2
                vhc_update(tb)
        def rfr():
            driver_alert()
            Vehicle_alert()
            
        self.mainFrame = Frame(master, width=950, background = 'grey')
        self.mainFrame.pack(fill=Y, expand=True)
        self.topFrame = Frame(self.mainFrame,width = 950, height=375, background="grey")
        self.topFrame.pack(fill=X, expand=True, side=TOP)
        self.bottomFrame = Frame(self.mainFrame,width = 950, height=375, background="grey")
        self.bottomFrame.pack(fill=X, expand=True, side=TOP)
        self.drvFrm = Frame(self.topFrame, height=40, bg='grey')
        self.drvFrm.pack(side=TOP,fill=X)
        self.drvLabel= Label(self.drvFrm, text= 'Driver', font = ('arial 14 bold'),fg='white',bg='grey')
        self.drvLabel.place(x=50, y=5)
        self.drvtableFrame = Frame(self.topFrame,width = 950, height=335, background="white")
        self.drvtableFrame.pack(fill=X, expand=True, side=TOP)
        
        self.vhcFrm = Frame(self.bottomFrame, height=40, bg='grey')
        self.vhcFrm.pack(side=TOP,fill=X)
        self.vhcLabel= Label(self.vhcFrm, text= 'Vehicle', font = ('arial 14 bold'),fg='white', bg='grey')
        self.vhcLabel.place(x=50, y=5)
        self.vhctableFrame = Frame(self.bottomFrame,width = 950, height=335, background="white")
        self.vhctableFrame.pack(fill=X, expand=True, side=TOP)
        
        # Scrollbar
        trv_scroll = Scrollbar(self.drvtableFrame)
        trv_scroll.grid(row=0, column=1, sticky="nsew", rowspan=2)
        
        self.trv = ttk.Treeview(self.drvtableFrame, columns = (1,2,3,4,5), show='headings', height=12, yscrollcommand = trv_scroll.set)
        self.trv.grid(column=0, row=0,sticky=W+N+S+E)
        self.trv.column(1, width=80, anchor="center")
        self.trv.heading(1, text='DriverID')
        self.trv.column(2, width=100, anchor="center")
        self.trv.heading(2, text='Name')
        self.trv.column(3, width=150, anchor="center")
        self.trv.heading(3, text='Tel')
        self.trv.column(4, width=160, anchor="center")
        self.trv.heading(4, text='Document')
        self.trv.column(5, width=160, anchor="center")
        self.trv.heading(5, text='Date')
        
        rfr_btn = Button(self.drvFrm, text= 'Refresh',width=6,command=rfr)
        rfr_btn.place(x=550)
        
        vhctrv_scroll = Scrollbar(self.vhctableFrame)
        vhctrv_scroll.grid(row=0, column=1, sticky="nsew", rowspan=2)
        
        self.vhctrv = ttk.Treeview(self.vhctableFrame, columns = (1,2,3,4), show='headings', height=12, yscrollcommand = trv_scroll.set)
        self.vhctrv.grid(column=0, row=0,sticky=W+N+S+E)
        self.vhctrv.column(1, width=80, anchor="center")
        self.vhctrv.heading(1, text='Reg No')
        self.vhctrv.column(2, width=100, anchor="center")
        self.vhctrv.heading(2, text='DriverID')
        self.vhctrv.column(3, width=150, anchor="center")
        self.vhctrv.heading(3, text='Documents')
        self.vhctrv.column(4, width=160, anchor="center")
        self.vhctrv.heading(4, text='Date')
        rfr()

        
