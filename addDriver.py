from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import mysql.connector
from datetime import date


class AddDriver():
    def __init__(self,master,mydb):
        self.mycursor = mydb.cursor()
        def update(rows):
            self.query_box.delete(*self.query_box.get_children())
            for i in rows:
                self.query_box.insert('','end', values=i)
        
        def search():
            self.mycursor = mydb.cursor()
            query = "SElECT Driver_ID, Firstname, Lastname,Phone, Status From driver WHERE Firstname LIKE '%"+self.ent_Search.get()+"%' OR Lastname LIKE '%"+self.ent_Search.get()+"%'"
            self.mycursor.execute(query)
            rows=self.mycursor.fetchall()
            
            update(rows)
            
        def clear():
            self.mycursor = mydb.cursor()
            query = "SElECT Driver_ID, Firstname, Lastname,Phone, Status From driver"
            self.mycursor.execute(query)
            rows=self.mycursor.fetchall()
            
            update(rows)
        def get_row(event):
            self.mycursor = mydb.cursor()
            rowid = self.query_box.identify_row(event.y)
            item=self.query_box.item(self.query_box.focus())
            query = "SELECT * FROM driver WHERE Driver_ID ="+str(item['values'][0])
            self.mycursor.execute(query)
            items = list(self.mycursor.fetchall()[0])   
            self.driver_ID.set(items[0])
            self.Fname.set(items[1])
            self.Lname.set(items[2])
            self.phone.set(items[3])
            self.email.set(items[4])
            self.postcode.set(items[5])
            self.CT.set(items[6])
            self.address.set(items[7])
            self.DL.set(items[8])
            self.ent_Exp_date.set_date(items[9])
            self.pco.set(items[10])
            self.ent_PCOExp_date.set_date(items[11])
            self.n_insurance.set(items[12])
            if items[13] == 'Off':
                self.ent_Status.current(1)
            
        def clear_entries():
            self.driver_ID.set("")
            self.Fname.set("")
            self.Lname.set("")
            self.phone.set("")
            self.email.set("")
            self.postcode.set("")
            self.CT.set("")
            self.address.set("")
            self.DL.set("")
            self.ent_Exp_date.set_date(date.today())
            self.pco.set("")
            self.ent_PCOExp_date.set_date(date.today())
            self.n_insurance.set("")
        def test():
            print(self.status.get())
            
        def update_driver():
            self.mycursor = mydb.cursor()
            pco_date = self.pco_exp.get()
            DL_date = self.DL_exp.get()
            if messagebox.askyesno("Confirm Please", "Are you sure you want to update this driver?"):
                query = """UPDATE driver SET Firstname = %s, Lastname= %s, Phone= %s, Email= %s,
                Postcode= %s, City= %s, Address= %s, DL_No= %s, DL_Exp= %s, PCO_No= %s, PCO_Exp= %s, National_Insurance= %s,
                Status= %s WHERE Driver_ID = %s"""
                self.mycursor.execute(query, (self.Fname.get(), self.Lname.get(), self.phone.get(), self.email.get(),
                                          self.postcode.get(), self.CT.get(), self.address.get(), self.DL.get(),
                                          DL_date, self.pco.get(), pco_date, self.n_insurance.get(),
                                          self.status.get(), self.driver_ID.get()))
                mydb.commit()
                self.mycursor.close()
                clear()
            else:
                return True
        def add_new():
            pco_date = self.pco_exp.get()
            DL_date = self.DL_exp.get()
            self.mycursor = mydb.cursor()
            query = """INSERT INTO driver VALUES (Null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            self.mycursor.execute(query, (self.Fname.get(), self.Lname.get(), self.phone.get(), self.email.get(),
                                          self.postcode.get(), self.CT.get(), self.address.get(), self.DL.get(),
                                          DL_date, self.pco.get(), pco_date, self.n_insurance.get(),
                                          self.status.get()))
            mydb.commit()
            self.mycursor.close()
            clear()
            
        def delete_driver():
            self.mycursor = mydb.cursor()
            driver = self.driver_ID.get()
            if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this Driver?"):
                query = "DELETE FROM driver WHERE Driver_ID = "+driver
                self.mycursor.execute(query)
                mydb.commit()
                self.mycursor.close()
                clear()
            else:
                return True
        def driver_validation(func):
            firstname = self.ent_Firstname.get()
            lastname = self.ent_Lastname.get()
            phone = self.ent_phone.get()
            email = self.ent_Email.get()
            postcode = self.ent_postcode.get()
            city = self.ent_CT.get()
            address = self.ent_address.get()
            dlicence = self.ent_DL.get()
            dlexpiry = self.ent_Exp_date.get()
            pco_no = self.ent_PCO.get()
            pco_expiry = self.ent_PCOExp_date.get()
            insurance = self.ent_NI.get()         

            if (any(not(x.isalpha()) for x in firstname)):
                messagebox.showerror(title = 'Error', message = 'Firstname contains invalid characters!')
            elif (any(not(x.isalpha()) for x in lastname)):
                messagebox.showerror(title = 'Error', message = 'Lastname contains invalid characters!')
            elif (any((not(x.isdigit())) for x in phone)):
                messagebox.showerror(title = 'Error', message = 'Phone contains invalid characters!')
            elif len(phone) != 11:
                messagebox.showerror(title = 'Error', message = 'Phone needs to contain 11 digits!')
            elif '@' and '.' not in email:
                messagebox.showerror(title = 'Error', message = 'Invalid Email!')    
            elif len(firstname) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Firstname!')
            elif len(lastname) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Lastname!')
            elif len(email) == 0 or email=='Enter Customer Email':
                messagebox.showerror(title = 'Error', message = 'Enter Email!')    
            elif len(city) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter City/Town!')
            elif len(address) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Address!')
            elif len(postcode) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Postcode!')
            elif len(dlicence) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Driver Licence No!')
            elif len(pco_no) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter PCO No!')
            elif len(insurance) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Insurance No!')
            else:
                if func == 'add':
                    add_new()
                elif func == 'update':
                    update_driver()
                elif func == 'delete':
                    delete_driver()
        def add_driver():
            driver_validation('add')
        def del_driver():
            driver_validation('delete')
        def upd_driver():
            driver_validation('update')
            
        self.mainFrame = Frame(master, width=950, background = 'yellow')
        self.mainFrame.pack(fill=Y, expand=True)
        self.topFrame = Frame(self.mainFrame,width = 950, height=100, background="blue")
        self.topFrame.pack(fill=X, expand=True, side=TOP)
        self.tableFrame= Frame(self.mainFrame, width=475, height = 600, background='black')
        self.tableFrame.pack(fill='both', expand=True, side=LEFT, pady=0)
        self.formFrame=Frame(self.mainFrame, width=475, height=600, background='#fcc324')
        self.formFrame.pack(fill='both', expand=True,side=LEFT, padx=0, pady=0)
        
        
        
        # Scrollbar
        query_scroll = Scrollbar(self.tableFrame)
        query_scroll.grid(row=0, column=1, sticky="nsew", rowspan=2)

        # Style configurations for ttk

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10))

        # Query output box

        self.query_box = ttk.Treeview(self.tableFrame,
                                 columns=('DriverID', 'Firstname','Lastname','Tel','Status'),height=25,yscrollcommand=query_scroll.set)
        self.query_box.grid(row=0, column=0)
        self.query_box["columns"] = ('DriverID', 'Firstname','Lastname','Tel','Status')
        self.query_box.column("DriverID", width=80, anchor="center")
        self.query_box.heading("DriverID", text="DriverID")
        self.query_box.column("Firstname", width=90, anchor="center")
        self.query_box.heading("Firstname", text="Firstname")
        self.query_box.column("Lastname", width=90, anchor="center")
        self.query_box.heading("Lastname", text="Lastname")
        self.query_box.column("Tel", width=120, anchor="center")
        self.query_box.heading("Tel", text="Tel")
        self.query_box.column("Status", width=80, anchor="center")
        self.query_box.heading("Status", text="Status")
        self.query_box["show"] = "headings"
        
        self.query_box.bind('<Double 1>', get_row)
        self.mycursor = mydb.cursor()
        query = "SElECT Driver_ID, Firstname, Lastname,Phone, Status From driver"
        self.mycursor.execute(query)
        rows = self.mycursor.fetchall()
        update(rows)
        
        

##################### Widgets ########################################################
        #Search
        self.search_query=StringVar()
        self.lbl_Search = Label(self.topFrame, text = 'Search: ', font='arial 12 bold', fg='white', bg='blue')
        self.lbl_Search.place(x=40, y=20)
        self.ent_Search = Entry(self.topFrame,width=30, bd=4, textvariable=self.search_query)
        self.ent_Search.place(x=150, y=20)
        
        self.search_btn = Button(self.topFrame, text= 'Search', width=6, command=search)
        self.search_btn.place(x=150, y=60)
        
        self.clr_btn = Button(self.topFrame, text= 'Clear',width=6,command=clear)
        self.clr_btn.place(x=250, y=60)
        
        self.clr_entries_btn = Button(self.topFrame, text= 'Clear Entries',width=9,command=clear_entries)
        self.clr_entries_btn.place(x=800, y=65)
        
        # Driver ID
        self.driver_ID = StringVar()
        self.lbl_driverID = Label(self.formFrame, text='Driver ID: ', font='arial 12 bold', fg='white',bg='#fcc324')
        self.lbl_driverID.place(x=40, y=5)
        self.ent_driverID = Entry(self.formFrame, width=30, bd=4, textvariable=self.driver_ID,state=DISABLED)
        self.ent_driverID.place(x=150, y=5)
        
        # FirstName
        self.Fname = StringVar()
        self.lbl_Firstname = Label(self.formFrame, text='Firstname:', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_Firstname.place(x=40, y=40)
        self.ent_Firstname = Entry(self.formFrame, width=30, bd=4,textvariable=self.Fname)
        self.ent_Firstname.place(x=150, y=40)
        # Lastname
        self.Lname = StringVar()
        self.lbl_Lastname = Label(self.formFrame, text='Lastname :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_Lastname.place(x=40, y=75)
        self.ent_Lastname = Entry(self.formFrame, width=30, bd=4,textvariable=self.Lname)
        self.ent_Lastname.place(x=150, y=75)
        
        # phone
        self.phone = StringVar()
        self.lbl_phone = Label(self.formFrame, text='Phone :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=110)
        self.ent_phone = Entry(self.formFrame, width=30, bd=4, textvariable=self.phone)
        self.ent_phone.place(x=150, y=110)
        
        #Email
        self.email = StringVar()
        self.lbl_Email = Label(self.formFrame, text='Email :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_Email.place(x=40, y=145)
        self.ent_Email = Entry(self.formFrame, width=30, bd=4, textvariable=self.email)
        self.ent_Email.place(x=150, y=145)

        #Postcode
        self.postcode = StringVar()
        self.lbl_postcode = Label(self.formFrame, text='Postcode :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_postcode.place(x=40, y=180)
        self.ent_postcode = Entry(self.formFrame, width=30, bd=4, textvariable=self.postcode)
        self.ent_postcode.place(x=150, y=180)
    
        #City/Town
        self.CT = StringVar()
        self.lbl_CT = Label(self.formFrame, text='City/Town :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_CT.place(x=40, y=215)
        self.ent_CT = Entry(self.formFrame, width=30, bd=4, textvariable=self.CT)
        self.ent_CT.place(x=150, y=215)

        #Address
        self.address = StringVar()
        self.lbl_address = Label(self.formFrame, text='Address :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_address.place(x=40, y=250)
        self.ent_address = Entry(self.formFrame, width=30, bd=4, textvariable=self.address)
        self.ent_address.place(x=150, y=250)
        
        # Driving Licence
        self.DL =  StringVar()
        self.lbl_DL=Label(self.formFrame,text='Licence :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_DL.place(x=40,y=285)
        self.ent_DL=Entry(self.formFrame,width=30,bd=4, textvariable=self.DL)
        self.ent_DL.place(x=150,y=285)
        
        #Driver Licence Expiry
        self.DL_exp = StringVar()
        self.lbl_Exp_date = Label(self.formFrame, text='DL Exp :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_Exp_date.place(x=40, y=320)
        self.ent_Exp_date = DateEntry(self.formFrame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, year=2021, textvariable=self.DL_exp, date_pattern='y-mm-dd')
        self.ent_Exp_date.place(x=150, y=320)
        
        # PCO Licence No
        self.pco = StringVar()
        self.lbl_PCO=Label(self.formFrame,text='PCO No :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_PCO.place(x=40,y=355)
        self.ent_PCO=Entry(self.formFrame,width=30,bd=4, textvariable=self.pco)
        self.ent_PCO.place(x=150,y=355)
        
        #PCO Expiry
        self.pco_exp = StringVar()
        self.lbl_PCOExp_date = Label(self.formFrame, text='PCO Exp :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_PCOExp_date.place(x=40, y=390)
        self.ent_PCOExp_date = DateEntry(self.formFrame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, year=2021, textvariable=self.pco_exp, date_pattern='y-mm-dd')
        self.ent_PCOExp_date.place(x=150, y=390)
        
        # National Insurance No
        self.n_insurance = StringVar()
        self.lbl_NI=Label(self.formFrame,text='NI No :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_NI.place(x=40,y=425)
        self.ent_NI=Entry(self.formFrame,width=30,bd=4, textvariable=self.n_insurance)
        self.ent_NI.place(x=150,y=425)
        
        #Status
        self.status = StringVar()
        self.lbl_Status = Label(self.formFrame, text='Status:', font='arial 12 bold', fg='white', bg='#fcc324',width=11,anchor=W)
        self.lbl_Status.place(x=40, y=460)
        self.ent_Status = ttk.Combobox(self.formFrame,values=['On','Off'],width=28, state='readonly', textvariable = self.status)
        self.ent_Status.place(x=150,y=460)
        self.ent_Status.current(0)
        
        #Add Button
        self.add_button=Button(self.formFrame,text='Add Driver', width=11,command=add_driver)
        self.add_button.place(x=40,y=490)
        
        #Update Buttontest
        self.upd_button=Button(self.formFrame,text='Update Driver',width=11,command=upd_driver)
        self.upd_button.place(x=170,y=490)
        
        #Delete Button
        self.del_button=Button(self.formFrame,text='Delete Driver',width=11, command=del_driver)
        self.del_button.place(x=300,y=490)


