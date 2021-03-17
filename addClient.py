from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import numpy as np
import mysql.connector

class AddClient():
    def __init__(self,master,mydb):
        def update(rows):
            self.trv.delete(*self.trv.get_children())
            for i in rows:
                self.trv.insert('','end', values=i)
        
        def search():
            self.mycursor = mydb.cursor()
            query = "SElECT Client_ID, Name, Phone, Email From client WHERE Name LIKE '%"+self.ent_Search.get()+"%' OR Client_ID LIKE '%"+self.ent_Search.get()+"%'"
            self.mycursor.execute(query)
            rows=self.mycursor.fetchall()
            update(rows)
            
        def clear():
            self.mycursor = mydb.cursor()
            query = "SElECT Client_ID, Name, Phone, Email From client"
            self.mycursor.execute(query)
            rows=self.mycursor.fetchall()
            update(rows)
        def get_row(event):
            self.mycursor = mydb.cursor()
            rowid = self.trv.identify_row(event.y)
            item=self.trv.item(self.trv.focus())
            query = "SELECT * FROM client WHERE Client_ID ="+str(item['values'][0])
            self.mycursor.execute(query)
            items = list(self.mycursor.fetchall()[0])
            self.ClientID.set(items[0])
            self.Name.set(items[1])
            self.phone.set(items[2])
            self.email.set(items[3])
            self.postcode.set(items[4])
            self.city.set(items[5])
            self.address.set(items[6])    
            
        def test():
            print(self.status.get())
            
        def update_client():
            self.mycursor = mydb.cursor()
            if messagebox.askyesno("Confirm Please", "Are you sure you want to update this client?"):
                query = """UPDATE client SET Name = %s, Phone= %s, Email= %s, Postcode= %s,City= %s, Address= %s WHERE Client_ID = %s"""
                self.mycursor.execute(query, (self.Name.get(), self.phone.get(), self.email.get(),self.postcode.get(),
                                              self.city.get(),self.address.get(), int(self.ClientID.get())))
                mydb.commit()
                self.mycursor.close()
                clear()
            else:
                return True
        def add_new():
            self.mycursor = mydb.cursor()
            query = """INSERT INTO client VALUES (Null, %s,%s,%s,%s,%s,%s)"""
            self.mycursor.execute(query, (self.Name.get(), self.phone.get(), self.email.get(),self.postcode.get(),
                                          self.city.get(),self.address.get()))
            mydb.commit()
            self.mycursor.close()
            clear()
        def delete_client():
            self.mycursor = mydb.cursor()
            client = self.ClientID.get()
            if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this client?"):
                query = "DELETE FROM client WHERE Client_ID = "+client
                self.mycursor.execute(query)
                mydb.commit()
                self.mycursor.close()
                clear()
            else:
                return True        
        
        def refresh():    
            self.ClientID.set('')
            self.Name.set('')
            self.phone.set('')
            self.email.set('')
            self.address.set('')
            self.city.set('')
            self.postcode.set('')
        def client_validation(func):
            name = self.ent_Name.get()
            phone = self.ent_phone.get()
            email = self.ent_Email.get()
            postcode = self.ent_postcode.get()
            city = self.ent_city.get()
            address = self.ent_address.get()

            if (any(not(x.isalpha()) and not(x.isspace()) for x in name)):
                messagebox.showerror(title = 'Error', message = 'Name contains invalid characters!')
            elif (any((not(x.isdigit())) for x in phone)):
                messagebox.showerror(title = 'Error', message = 'Phone contains invalid characters!')
            elif len(phone) != 11:
                messagebox.showerror(title = 'Error', message = 'Phone needs to contain 11 digits!')
            elif '@' and '.' not in email:
                messagebox.showerror(title = 'Error', message = 'Invalid Email!')    
            elif len(name) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Client Name!')
            elif len(email) == 0 or name=='Enter Customer Email':
                messagebox.showerror(title = 'Error', message = 'Enter Email!')    
            elif len(city) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter City/Town!')
            elif len(address) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Address!')
            elif len(postcode) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Postcode!')

            else:
                if func == 'add':
                    add_new()
                elif func == 'update':
                    update_client()
                elif func == 'delete':
                    delete_client()
        def add_client():
            client_validation('add')
        def del_client():
            client_validation('delete')
        def upd_client():
            client_validation('update')
        self.mainFrame = Frame(master, width=950, background = 'yellow')
        self.mainFrame.pack(fill=Y, expand=True)
        self.topFrame = Frame(self.mainFrame,width = 950, height=100, background="blue")
        self.topFrame.pack(fill=X, expand=True, side=TOP)
        self.tableFrame= Frame(self.mainFrame, width=475, height = 600, background='black')
        self.tableFrame.pack(fill='both', expand=True, side=LEFT, pady=0)
        self.formFrame=Frame(self.mainFrame, width=475, height=600, background='#fcc324')
        self.formFrame.pack(fill='both', expand=True,side=LEFT, padx=0, pady=0)
        
        # Scrollbar
        trv_scroll = Scrollbar(self.tableFrame)
        trv_scroll.grid(row=0, column=1, sticky="nsew", rowspan=2)
        
        self.trv = ttk.Treeview(self.tableFrame, columns = (1,2,3,4), show='headings', height=25, yscrollcommand = trv_scroll.set)
        self.trv.grid(column=0, row=0,sticky=W+N+S+E)
        self.trv.column(1, width=80, anchor="center")
        self.trv.heading(1, text='ClientID')
        self.trv.column(2, width=100, anchor="center")
        self.trv.heading(2, text='Client Name')
        self.trv.column(3, width=150, anchor="center")
        self.trv.heading(3, text='Tel')
        self.trv.column(4, width=160, anchor="center")
        self.trv.heading(4, text='Email')
        
        self.trv.bind('<Double 1>', get_row)
        
        self.mycursor = mydb.cursor()
        query = "SElECT Client_ID, Name, Phone, Email From client"
        self.mycursor.execute(query)
        rows = self.mycursor.fetchall()
        update(rows)        

####################################### Widgets #######################################################################################       
        #Search
        self.lbl_Search = Label(self.topFrame, text = 'Search: ', font='arial 12 bold', fg='white', bg='blue')
        self.lbl_Search.place(x=40, y=20)
        self.ent_Search = Entry(self.topFrame,width=30, bd=4)
        self.ent_Search.place(x=150, y=20)
        
        self.search_btn = Button(self.topFrame, text= 'Search', width=6, command=search)
        self.search_btn.place(x=150, y=60)
        
        self.clr_btn = Button(self.topFrame, text= 'Clear',width=6,command=clear)
        self.clr_btn.place(x=250, y=60)
        
        #Refresh Label
        self.rfr_btn = Button(self.formFrame, text= 'Clear Entries', command=refresh)
        self.rfr_btn.place(x=330, y=10)        
        
        #Client ID
        self.ClientID = StringVar()
        self.lbl_ClientID = Label(self.formFrame,text='Client ID :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_ClientID.place(x=40, y=40)
        self.ent_ClientID = Entry(self.formFrame,width=30,bd=4, textvariable = self.ClientID, state=DISABLED)
        self.ent_ClientID.place(x=150,y=45)
        
        #Client Name
        self.Name = StringVar()
        self.lbl_Name = Label(self.formFrame,text='Name :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_Name.place(x=40, y=80)
        self.ent_Name = Entry(self.formFrame,width=30,bd=4, textvariable = self.Name)
        self.ent_Name.place(x=150,y=85)
        

        # phone
        self.phone = StringVar()
        self.lbl_phone = Label(self.formFrame, text='Phone :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=120)
        self.ent_phone = Entry(self.formFrame, width=30, bd=4, textvariable = self.phone)
        self.ent_phone.place(x=150, y=125)
        
        #Email
        self.email = StringVar()
        self.lbl_Email = Label(self.formFrame, text='Email :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_Email.place(x=40, y=160)
        self.ent_Email = Entry(self.formFrame, width=30, bd=4, textvariable = self.email)
        self.ent_Email.place(x=150, y=165)
        
        #City/Town
        self.city = StringVar()
        self.lbl_city=Label(self.formFrame,text='City/Town :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_city.place(x=40,y=200)
        self.ent_city=Entry(self.formFrame, width=30, bd=4, textvariable = self.city)
        self.ent_city.place(x=150,y=205)
        
        #postcode
        self.postcode = StringVar()
        self.lbl_postcode = Label(self.formFrame, text='Postcode :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_postcode.place(x=40, y=240)
        self.ent_postcode = Entry(self.formFrame, width=30, bd=4, textvariable = self.postcode)
        self.ent_postcode.place(x=150, y=245)
        #Address
        self.address = StringVar()
        self.lbl_address=Label(self.formFrame,text='Address :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_address.place(x=40,y=280)
        self.ent_address=Entry(self.formFrame,width=30,bd=4, textvariable = self.address)
        self.ent_address.place(x=150,y=285)
        

        
         #Add Button
        self.add_button=Button(self.formFrame,text='Add Client', width =11, command = add_client)
        self.add_button.place(x=40,y=470)
        
        #Update Button
        self.upd_button=Button(self.formFrame,text='Update Client',width=11, command = upd_client)
        self.upd_button.place(x=170,y=470)
        
        #Delete Button
        self.del_button=Button(self.formFrame,text='Delete Client',width=11, command = del_client)
        self.del_button.place(x=300,y=470)
        
