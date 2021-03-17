from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import numpy as np
import mysql.connector

class AddBooking():
    def __init__(self, master,mydb):
        self.mydb = mydb             
        #Frames for Booking Tab
        OptionFrame = Frame(master, bg='black', height=250)
        OptionFrame.pack(fill='x',expand=True)
        BookingFrame = Frame(master, bg='blue',height=500)
        BookingFrame.pack(fill='x',expand=True)
        def crefresh_filter():
            #Client Add
            self.client_options = ['All Clients']
            self.client_ids = []
            self.mycursor=mydb.cursor()
            query = "Select Client_ID, Name, Phone from client"
            self.mycursor.execute(query)
            self.myids = self.mycursor.fetchall()
            mydb.commit()
            for client in self.myids:
                self.client_ids.append(client[0])
                self.client_options.append(str(client[0]) + ' - '+client[1]+'('+client[2]+')')
            self.ent_clientID['values'] = self.client_options
            drefresh_filter()
        def drefresh_filter():
            self.options=['All Drivers']
            self.just_ids = []
            self.mycursor = mydb.cursor()
            q="Select Driver_ID, Firstname from driver"
            self.mycursor.execute(q)
            self.ids=self.mycursor.fetchall()
            mydb.commit()
            for i in self.ids:
                self.just_ids.append(i[0])
                self.options.append(str(i[0]) +'-'+i[1])
            self.ent_driverID['values'] = self.options
            
        def update_filt(rows):
            self.query_box.delete(*self.query_box.get_children())
            for i in rows:
                self.query_box.insert('','end', values=i)
        def clear_filt():
            self.mycursor = self.mydb.cursor()
            query = """select booking.BookingID, client.Name, customer.Name,
            customer.Phone, driver.Firstname, booking.Job_Date, booking.Time, booking.Pick_Up_Address,
            booking.Drop_Off_Address, booking.Price,booking.Job_Status from booking
            Join client on booking.Client_ID = client.Client_ID
            Join driver on booking.Driver_ID = driver.Driver_ID
            Join customer on booking.CustomerID = customer.CustomerID"""
            self.mycursor.execute(query)
            rows=self.mycursor.fetchall()
            update_filt(rows)
        def search():
            self.mycursor = self.mydb.cursor()
            query = """select booking.BookingID, client.Name, customer.Name,
            customer.Phone, driver.Firstname, booking.Job_Date, booking.Time, booking.Pick_Up_Address,
            booking.Drop_Off_Address, booking.Price,booking.Job_Status from booking
            Join client on booking.Client_ID = client.Client_ID
            Join driver on booking.Driver_ID = driver.Driver_ID
            Join customer on booking.CustomerID = customer.CustomerID WHERE customer.Name LIKE %s OR client.Name LIKE %s"""
            self.mycursor.execute(query,("%"+self.ent_Search.get() + "%","%"+self.ent_Search.get() + "%"))
            rows=self.mycursor.fetchall()
            self.mydb.commit()
            update_filt(rows)
        def client_filt():
            if self.ent_clientID.get() == 'All Clients':
                return 'client.Client_ID'
            else:
                return self.ent_clientID.get()[0]
        def driver_filt():
            if self.ent_driverID.get()== 'All Drivers':
                return 'driver.Driver_ID'
            else:
                dID = self.ent_driverID.get()
                return dID[0:dID.index('-')]
                
        def status_filt():
            if self.ent_Status_filt.get()== 'All':
                return 'booking.Job_Status'
            else:
                return f"'{self.ent_Status_filt.get()}'"

        def final_filt():
            self.mycusor = self.mydb.cursor()
            #clear_filt()
            job_from_date = self.ent_from_date.get()
            job_to_date = self.ent_to_date.get()
            x= driver_filt()
            y= client_filt()
            #print(f"Where (booking.Job_Date>= '{job_from_date}' AND booking.Job_Date<= '{job_to_date}') booking.Job_Status = {status_filt()} And client.Client_ID = {y} AND driver.Driver_ID={x}")
            query = f"""select booking.BookingID, client.Name, customer.Name,
            customer.Phone, driver.Firstname, booking.Job_Date, booking.Time, booking.Pick_Up_Address,
            booking.Drop_Off_Address, booking.Price,booking.Job_Status from booking
            Join client on booking.Client_ID = client.Client_ID
            Join driver on booking.Driver_ID = driver.Driver_ID
            Join customer on booking.CustomerID = customer.CustomerID
            Where (booking.Job_Date>= '{job_from_date}' AND booking.Job_Date<= '{job_to_date}') And booking.Job_Status = {status_filt()} And client.Client_ID = {y} AND driver.Driver_ID={x}"""
            self.mycursor.execute(query)
            rows=self.mycursor.fetchall()
            update_filt(rows)
        #Search Bar
        self.search_query=StringVar(master)
        self.lbl_Search = Label(OptionFrame, text = 'Search: ', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_Search.place(x=40, y=20)
        self.ent_Search = Entry(OptionFrame,width=30, bd=4, textvariable=self.search_query)
        self.ent_Search.place(x=150, y=20)
        
        #Creating Buttons in OptionFrame
        self.search_btn = Button(OptionFrame, text= 'Search', width=6, command = search)
        self.search_btn.place(x=150, y=60)
        
        self.clr_btn = Button(OptionFrame, text= 'Clear',width=6, command = self.clear)
        self.clr_btn.place(x=250, y=60)
        
        #Driver filter
        self.lbl_driverID = Label(OptionFrame, text='Driver ID:', font='arial 12 bold', fg='white', bg='#fcc324',width=11,anchor=W)
        self.lbl_driverID.place(x=500, y=20)
        self.ent_driverID = ttk.Combobox(OptionFrame,width=28, state='readonly',values=['All Drivers'])
        drefresh_filter()
        self.ent_driverID.place(x=700,y=20)
        self.ent_driverID.current(0)
        
        #Client filter
        self.lbl_clientID = Label(OptionFrame, text='Client ID:', font='arial 12 bold', fg='white', bg='#fcc324',width=11,anchor=W)
        self.lbl_clientID.place(x=500, y=60)
        self.ent_clientID = ttk.Combobox(OptionFrame,width=28, state='readonly')
        self.ent_clientID['values'] = ['All']
        crefresh_filter()
        self.ent_clientID.place(x=700,y=60)
        self.ent_clientID.current(0)
        
        #From Date
        self.lbl_from_date = Label(OptionFrame, text='From :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_from_date.place(x=40, y=140)
        self.ent_from_date = DateEntry(OptionFrame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, year=2019, month=1, date_pattern='y-mm-dd')
        self.ent_from_date.place(x=200, y=140)
        
        #To Date
        self.lbl_to_date = Label(OptionFrame, text='To :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_to_date.place(x=40, y=180)
        self.ent_to_date = DateEntry(OptionFrame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, year=2021, date_pattern='y-mm-dd')
        self.ent_to_date.place(x=200, y=180)
        
        #Status
        self.status = StringVar()
        self.lbl_Status_filt = Label(OptionFrame, text='Status:', font='arial 12 bold', fg='white', bg='#fcc324',width=11,anchor=W)
        self.lbl_Status_filt.place(x=500, y=140)
        self.ent_Status_filt = ttk.Combobox(OptionFrame,values=['All','Not Assigned','Pending','Completed'],width=28, state='readonly', textvariable = self.status)
        self.ent_Status_filt.place(x=700,y=140)
        self.ent_Status_filt.current(0)
        
        self.btnbook= Button(OptionFrame,text='Make Booking',font='arial 12 bold',width=12, command = self.makeBooking)
        self.btnbook.place(x=1200,y=10)
        self.filt= Button(OptionFrame,text='Filter',font='arial 12 bold',width=12, command = final_filt)
        self.filt.place(x=1200,y=60)
        self.rfr= Button(OptionFrame,text='Refresh',font='arial 12 bold',width=12, command = crefresh_filter)
        self.rfr.place(x=1200,y=110)
              
        #Creating A table

        # Scrollbar
        query_scroll = Scrollbar(BookingFrame)
        query_scroll.grid(row=0, column=1, sticky="nsew", rowspan=2)

        # Style configurations for ttk
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10))

        # Query output box
        self.query_box = ttk.Treeview(BookingFrame,height=19,show='headings',
                                      yscrollcommand=query_scroll.set)
        self.query_box["columns"] = (1,2,3,4,5,6,7,8,9,10,11)
        self.query_box.grid(row=0, column=0)
        self.query_box.column(1, width=80, anchor="center")
        self.query_box.heading(1, text="BookingID")
        self.query_box.column(2, width=120, anchor="center")
        self.query_box.heading(2, text="Client")
        self.query_box.column(3, width=150, anchor="center")
        self.query_box.heading(3, text="Customer Name")
        self.query_box.column(4, width=100, anchor="center")
        self.query_box.heading(4, text="Phone")
        self.query_box.column(5, width=84, anchor="center")
        self.query_box.heading(5, text="Driver")
        self.query_box.column(6, width=100, anchor="center")
        self.query_box.heading(6, text="Job Date")
        self.query_box.column(7, width=80, anchor="center")
        self.query_box.heading(7, text="Time")
        self.query_box.column(8, width=210, anchor="center")
        self.query_box.heading(8, text="Pick-up")
        self.query_box.column(9, width=210, anchor="center")
        self.query_box.heading(9, text="Drop-off")
        self.query_box.column(10, width=80, anchor="center")
        self.query_box.heading(10, text="Price(£)")
        self.query_box.column(11, width=100, anchor="center")
        self.query_box.heading(11, text="Status")
        

        query_scroll.config(command=self.query_box.yview)
        
        #Importing data from sql for the table
        self.query_box.bind('<Double 1>', self.get_row)
        self.mycursor = self.mydb.cursor()
        query = """select booking.BookingID, client.Name, customer.Name,
        customer.Phone, driver.Firstname, booking.Job_Date, booking.Time, booking.Pick_Up_Address,
        booking.Drop_Off_Address, booking.Price,booking.Job_Status from booking
        Join client on booking.Client_ID = client.Client_ID
        Join driver on booking.Driver_ID = driver.Driver_ID
        Join customer on booking.CustomerID = customer.CustomerID"""
        self.mycursor.execute(query)
        rows = self.mycursor.fetchall()
        self.update(rows)
        #######################Frames#######################
    def makeBooking(self):

        self.master = Tk() 
        self.master.configure(bg='white')
        self.master.option_add('*Font', 'Goergia 12') #font for all widgets
        self.master.option_add('*Background', 'ivory2')#background of all widgets
        self.master.option_add('*Label.Font', 'helvetica 14') #font for all labels
        self.master.geometry("1000x750+200+50")
        self.master.title("Make Booking")
        self.master.resizable(False,False)

        
        #Top Frame
        self.topFrame= Frame(self.master,height=150,bg='white')
        self.topFrame.pack(fill=X)
        #Bottom Frame
        self.bottomFrame= Frame(self.master,height=600,bg='#fcc324')
        self.bottomFrame.pack(fill=X)
        #heading, image
        #self.top_image= PhotoImage(file='icons/addperson.png')
        top_image_lbl=Label(self.topFrame,bg='white')
        top_image_lbl.place(x=120,y=10)
        heading=Label(self.topFrame, text='  Make Booking ',font='arial 22 bold',fg='#003f8a',bg='white')
        heading.place(x=290,y=60)

        ###########################################Entries and Labels########################3

        #Account Type
        self.lbl_AccType = Label(self.bottomFrame, text='Client:', font='arial 12 bold', fg='white', bg='#fcc324',width=11,anchor=W)
        self.lbl_AccType.place(x=40, y=40)
        self.ent_type = ttk.Combobox(self.bottomFrame,width=28, state='readonly')
        self.ent_type['values'] = ['Select Client']
        self.ent_type.place(x=150,y=45)
        self.ent_type.current(0)
        
        # Driver ID
        self.lbl_driverID = Label(self.bottomFrame, text='Driver ID:', font='arial 12 bold', fg='white', bg='#fcc324',width=11,anchor=W)
        self.lbl_driverID.place(x=40, y=280)
        self.ent_driverID = ttk.Combobox(self.bottomFrame,width=28, state='readonly',values=['Select Driver'])
        self.refresh()
        self.ent_driverID.place(x=150,y=285)
        self.ent_driverID.current(0)
        
        #passenger name
        self.name = StringVar(self.master)
        self.lbl_name=Label(self.bottomFrame,text='Name :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_name.place(x=40,y=80)
        self.ent_name=Entry(self.bottomFrame,width=30,bd=4, textvariable=self.name)
        self.ent_name.insert(0,'Please enter Customer name')
        self.ent_name.place(x=150,y=85)
        # phone
        self.phone=StringVar(self.master)
        self.lbl_phone = Label(self.bottomFrame, text='Phone :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=120)
        self.ent_phone = Entry(self.bottomFrame, width=30, bd=4, textvariable=self.phone)
        self.ent_phone.insert(0, 'Please enter Customer Phone')
        self.ent_phone.place(x=150, y=125)
        
        #Email
        self.email = StringVar(self.master)
        self.lbl_Email = Label(self.bottomFrame, text='Email :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_Email.place(x=40, y=160)
        self.ent_Email = Entry(self.bottomFrame, width=30, bd=4, textvariable=self.email)
        self.ent_Email.insert(0, 'Enter Customer Email')
        self.ent_Email.place(x=150, y=165)
        
        #Date
        self.lbl_date = Label(self.bottomFrame, text='Date :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_date.place(x=40, y=200)
        self.ent_date = DateEntry(self.bottomFrame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, year=2020, date_pattern='y-mm-dd')
        self.ent_date.place(x=150, y=205)
        
        #Time
        self.lbl_time = Label(self.bottomFrame, text='Time :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_time.place(x=40, y=240)
        self.hourstr=StringVar(self.master,'10')
        self.hour = ttk.Combobox(self.bottomFrame,values=np.arange(24).tolist(),textvariable=self.hourstr,width=3,state="readonly")
        self.minstr=StringVar(self.master,'30')
        self.minstr.trace("w",self.trace_var)
        self.last_value = ""
        self.min = ttk.Combobox(self.bottomFrame,values=np.arange(0,60,5).tolist(),textvariable=self.minstr,width=3,state="readonly")
        self.hour.place(x=150,y=245)
        self.min.place(x=210,y=245)
        
        
        #Pick Up Address  
        self.lbl_pickUp=Label(self.bottomFrame,text='Pick-up Address :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_pickUp.place(x=500,y=40)
        self.ent_pickUp=Text(self.bottomFrame,width=30,bd=4,height=2)
        self.ent_pickUp.place(x=650,y=45)
        
        #Drop Off Address
        self.lbl_dropOff=Label(self.bottomFrame,text='Drop-off Address :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_dropOff.place(x=500,y=95)
        self.ent_dropOff=Text(self.bottomFrame,width=30,bd=4,height=2)
        self.ent_dropOff.place(x=650,y=100)
        
        #Number of Passengers
        self.passNo = StringVar(self.master)
        self.lbl_passNo = Label(self.bottomFrame, text='No of Passengers :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_passNo.place(x=500, y=150)
        self.ent_passNo = Entry(self.bottomFrame, width=30, bd=4, textvariable=self.passNo)
        self.ent_passNo.place(x=650, y=155)
        
        #Luggage
        self.Lugg = StringVar(self.master)
        self.lbl_Lugg = Label(self.bottomFrame, text='Luggage :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_Lugg.place(x=500, y=190)
        self.ent_Lugg = Entry(self.bottomFrame, width=30, bd=4, textvariable=self.Lugg)
        self.ent_Lugg.place(x=650, y=195)
        
        #Additional Information
        self.lbl_AddInfo=Label(self.bottomFrame,text='Addition Info :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_AddInfo.place(x=500,y=230)
        self.ent_AddInfo=Text(self.bottomFrame,width=30,bd=4,height=3)
        self.ent_AddInfo.place(x=650,y=235)
        
        #Rate Per Mile (£)
        self.rate = StringVar(self.master)
        self.lbl_RperMile = Label(self.bottomFrame, text='Rate (£) :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_RperMile.place(x=40, y=340)
        self.ent_RperMile = Entry(self.bottomFrame, width=15, bd=4, textvariable=self.rate)  
        self.ent_RperMile.place(x=150, y=345)
        
        #Distance
        self.distance = StringVar(self.master)
        self.lbl_Tdistance = Label(self.bottomFrame, text='Distance :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_Tdistance.place(x=310, y=340)
        self.ent_Tdistance = Entry(self.bottomFrame, width=15, bd=4, textvariable=self.distance)
        self.ent_Tdistance.place(x=420, y=345)
        
        #Total Price
        self.T_Price = StringVar(self.master,'0')
        self.lbl_Tprice = Label(self.bottomFrame, text='Total Price(£) :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_Tprice.place(x=40, y=400)
        self.ent_Tprice = Entry(self.bottomFrame, width=15, bd=4,textvariable=self.T_Price,state=DISABLED)
        #self.ent_RperMile.insert(0, 'Amount of Luggage')
        self.ent_Tprice.place(x=150, y=405)
        
        #Calculate Price
        calBtn=Button(self.bottomFrame,text='Calculate Price',command=self.calculating_price)
        calBtn.place(x=310,y=420)

        
        #Status
        self.lbl_status = Label(self.bottomFrame, text='Status :', font='arial 14 bold', fg='white', bg='#fcc324')
        self.lbl_status.place(x=650, y=320)
        self.ent_status = ttk.Combobox(self.bottomFrame,width=15, state='readonly',values=['Not Assigned','Pending','Completed'])
        self.ent_status.place(x=800,y=320)
        self.ent_status.current(0)
        
        #BookingID
        self.BookingID = StringVar(self.master)
        self.lbl_BookingID = Label(self.bottomFrame, text='Booking ID: ', font='arial 12 bold', fg='white',bg='#fcc324')
        self.lbl_BookingID.place(x=650, y=360)
        self.ent_BookingID = Entry(self.bottomFrame, width=15, bd=4, textvariable=self.BookingID,state=DISABLED)
        self.ent_BookingID.place(x=800, y=360)
        
        #Add Button
        self.add_button=Button(self.bottomFrame,text='Add Booking', width =12,command=self.add_booking, state = 'normal')
        self.add_button.place(x=300,y=520)
        
        #Update Button
        self.upd_button=Button(self.bottomFrame,text='Update Booking',width=12,command = self.upd_booking, state = 'disabled')
        self.upd_button.place(x=440,y=520)
        
        #Delete Button
        self.del_button=Button(self.bottomFrame,text='Delete Booking',width=12,command = self.del_booking, state = 'disabled')
        self.del_button.place(x=580,y=520)
        self.refresh()
        #master.mainloop()
    def update(self,rows):
        self.query_box.delete(*self.query_box.get_children())
        for i in rows:
            self.query_box.insert('','end', values=i)
        
    def clear(self):
        self.mycursor = self.mydb.cursor()
        query = """select booking.BookingID, client.Name, customer.Name,
        customer.Phone, driver.Firstname, booking.Job_Date, booking.Time, booking.Pick_Up_Address,
        booking.Drop_Off_Address, booking.Price,booking.Job_Status from booking
        Join client on booking.Client_ID = client.Client_ID
        Join driver on booking.Driver_ID = driver.Driver_ID
        Join customer on booking.CustomerID = customer.CustomerID"""
        self.mycursor.execute(query)
        rows=self.mycursor.fetchall()
        self.update(rows)
        
    def get_row(self,event):
        self.makeBooking()
        self.upd_button.config(state='normal')
        self.del_button.config(state='normal')
        self.add_button.config(state='disabled')
        self.mycursor = self.mydb.cursor()
        rowid = self.query_box.identify_row(event.y)
        item=self.query_box.item(self.query_box.focus())
        query = "SELECT * FROM booking WHERE BookingID ="+str(item['values'][0])
        self.mycursor.execute(query)
        items = list(self.mycursor.fetchall()[0])
        self.BookingID.set(items[0])
        #print(items[1])
        self.ent_type.current(self.client_ids.index(int(items[1]))+1)
        self.mycursor = self.mydb.cursor()
        q = "Select Name, Phone,Email From customer Where CustomerID = "+str(items[2])
        self.mycursor.execute(q)
        cust_data = self.mycursor.fetchall()
        self.mydb.commit()
        self.mycursor.close()
        self.name.set(cust_data[0][0])
        self.phone.set(cust_data[0][1])
        self.email.set(cust_data[0][2])
        self.ent_driverID.current(self.just_ids.index(int(items[3]))+1)
        self.ent_date.set_date(items[4])
        #print(items[12])
        self.hourstr.set(items[5].split(':')[0])
        self.minstr.set(items[5].split(':')[1])
        self.ent_pickUp.insert(END, items[6])
        self.ent_dropOff.insert(END, items[7])
        self.passNo.set(items[8])
        self.Lugg.set(items[9])
        self.ent_AddInfo.insert(END, items[10])
        self.T_Price.set(items[11])
        self.rate.set(items[12])
        self.distance.set(items[13])
        status_list= ['Not Assigned','Pending','Completed']
        self.ent_status.current(status_list.index(items[14]))
        self.mycursor = self.mydb.cursor()
        q = "Select CustomerID from customer Where Name = %s and Phone= %s"
        self.mycursor.execute(q, (self.name.get(), self.phone.get()))
        self.cust_id = self.mycursor.fetchall()
        self.mydb.commit()
        self.mycursor.close()
        #print(self.cust_id)
  
    def test(self):
        print(self.client_ids)

    def update_booking(self):
        self.mycursor = self.mydb.cursor()
        job_date = self.ent_date.get()
        job_time = self.hourstr.get() + ':'+self.minstr.get()+':00'

        if messagebox.askyesno("Confirm Please", "Are you sure you want to update this booking?"):
            query = """UPDATE booking SET Client_ID = %s, CustomerID= %s, Driver_ID= %s, Job_Date= %s,
            Time= %s, Pick_Up_Address= %s, Drop_Off_Address= %s, NoOfPassengers= %s, Luggage= %s,
            Additional_Info= %s, Price= %s,Rate =%s, Distance= %s, Job_Status= %s WHERE BookingID = %s"""
            self.mycursor.execute(query, (self.ent_type.get()[0],self.cust_id[0][0], self.ent_driverID.get()[0],
                                          job_date, job_time, self.ent_pickUp.get(1.0,'end-1c'), self.ent_dropOff.get(1.0,'end-1c'),
                                          self.passNo.get(), self.Lugg.get(), self.ent_AddInfo.get(1.0,'end-1c'), self.T_Price.get(),
                                          self.ent_RperMile.get(), self.ent_Tdistance.get(), self.ent_status.get(),self.BookingID.get()))
            self.mydb.commit()
            self.mycursor.close()
            self.mycursor = self.mydb.cursor()
            cust_query = """UPDATE customer SET Name = %s, Phone= %s, Email= %s WHERE CustomerID = %s"""
            self.mycursor.execute(cust_query, (self.name.get(), self.phone.get(), self.email.get(), self.cust_id[0][0]))
            self.mydb.commit()
            self.mycursor.close()
            self.clear()
            self.mycursor.close()
            self.master.destroy()
            
        else:
            return True
    def add_new(self):
        #Coverting Date obtained into SQL format
        job_date = self.ent_date.get()
        job_time = self.hourstr.get() + ':'+self.minstr.get()+':00'
        
        #Inserting Customer first as CustomerID will be needed for the next step
        self.mycursor=self.mydb.cursor()
        query = "INSERT INTO customer VALUES (Null,%s,%s,%s)"
        self.mycursor.execute(query, (self.name.get(), self.phone.get(), self.email.get()))
        self.mydb.commit()
        self.mycursor.close()
        #Obtaining the customerID to insert into 'booking' table
        self.mycursor=self.mydb.cursor()
        q = "Select CustomerID from customer Where Name = %s and Phone= %s"
        self.mycursor.execute(q, (self.name.get(), self.phone.get()))
        cust_id = self.mycursor.fetchall()
        self.mydb.commit()
        self.mycursor.close()
        
        #Inserting data from form into the booking table.
        self.mycursor = self.mydb.cursor()
        query = """INSERT INTO booking VALUES (Null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        self.mycursor.execute(query, (self.ent_type.get()[0],cust_id[0][0], self.ent_driverID.get()[0],
                                      job_date, job_time, self.ent_pickUp.get(1.0,'end-1c'), self.ent_dropOff.get(1.0,'end-1c'),
                                      self.passNo.get(), self.Lugg.get(), self.ent_AddInfo.get(1.0,'end-1c'), self.T_Price.get(),
                                      self.ent_RperMile.get(), self.ent_Tdistance.get(),self.ent_status.get()))
        self.mydb.commit()
        self.mycursor.close()
        self.clear()
        self.master.destroy()      
        
    def validation(self,func):
        client = self.ent_type.get()
        name = self.ent_name.get()
        phone = self.ent_phone.get()
        email = self.ent_Email.get()
        driver = self.ent_driverID.get()
        pickup = self.ent_pickUp.get(1.0,'end-1c')
        dropoff = self.ent_dropOff.get(1.0,'end-1c')
        passengers = self.ent_passNo.get()
        addInfo = self.ent_AddInfo.get(1.0,'end-1c')
        luggage = self.ent_Lugg.get()
        
        if client == 'Select Client':
            messagebox.showerror(title = 'Error', message = 'Client is not selected!')
        elif (any(not(x.isalpha()) and not(x.isspace()) for x in name)):
            messagebox.showerror(title = 'Error', message = 'Name contains invalid characters!')
        elif (any((not(x.isdigit())) for x in phone)):
            messagebox.showerror(title = 'Error', message = 'Phone contains invalid characters!')
        elif len(phone) != 11 or phone == 'Please enter Customer Phone':
            messagebox.showerror(title = 'Error', message = 'Phone needs to contain 11 digits!')
        elif '@' and '.' not in email:
            messagebox.showerror(title = 'Error', message = 'Invalid Email!')    
        elif driver == 'Select Driver':
            messagebox.showerror(title = 'Error', message = 'Driver is not selected!')
        elif len(name) == 0 or name=='Please enter Customer name':
            messagebox.showerror(title = 'Error', message = 'Enter Customer Name!')
        elif len(email) == 0 or name=='Enter Customer Email':
            messagebox.showerror(title = 'Error', message = 'Enter Email!')    

        elif len(pickup) == 0:
            messagebox.showerror(title = 'Error', message = 'Enter Pickup Address!')
        elif len(dropoff) == 0:
            messagebox.showerror(title = 'Error', message = 'Enter Dropoff Address!')
        elif len(passengers) == 0:
            messagebox.showerror(title = 'Error', message = 'Enter number of passengers!')
        else:
            if func == 'add':
                self.add_new()
            elif func == 'update':
                self.update_booking()
            elif func == 'delete':
                self.delete_booking()
            

    def add_booking(self):
        self.validation('add')
    def del_booking(self):
        self.validation('delete')
    def upd_booking(self):
        self.validation('update')
    

    def delete_booking(self):
        self.mycursor = self.mydb.cursor()
        booking = self.BookingID.get()
        if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this Booking?"):
            query = "DELETE FROM booking WHERE BookingID = "+booking
            self.mycursor.execute(query)
            self.mydb.commit()
            self.mycursor.close()
            self.clear()
            self.master.destroy()
        else:
            return True 
    def refresh(self):
        #Driver Add
        self.options=['Select Driver']
        self.just_ids = []
        self.mycursor = self.mydb.cursor()
        q="Select Driver_ID, Firstname from driver"
        self.mycursor.execute(q)
        self.ids=self.mycursor.fetchall()
        self.mydb.commit()
        self.mycursor.close()
        for i in self.ids:
            self.just_ids.append(i[0])
            self.options.append(str(i[0]) +' - '+i[1])
        self.ent_driverID['values'] = self.options
        #Client Add
        self.client_options = ['Select Client']
        self.client_ids = []
        self.mycursor=self.mydb.cursor()
        query = "Select Client_ID, Name, Phone from client"
        self.mycursor.execute(query)
        self.myids = self.mycursor.fetchall()
        self.mydb.commit()
        self.mycursor.close()
        for client in self.myids:
            self.client_ids.append(client[0])
            self.client_options.append(str(client[0]) + ' - '+client[1]+'('+client[2]+')')
        self.ent_type['values'] = self.client_options
        
    def trace_var(self,*args):
        if self.last_value == "59" and self.minstr.get() == "0":
            self.hourstr.set(int(self.hourstr.get())+1 if self.hourstr.get() !="23" else 0)
        self.last_value = self.minstr.get()

    def calculating_price(self):
        rate = self.ent_RperMile.get()
        distance = self.ent_Tdistance.get()
        if len(rate) == 0:
            messagebox.showerror(title = 'Error', message = 'Enter Rate!')
        elif (any((not(y.isdigit() or '.' in y)) for y in rate)) or rate.count('.')>1:
            messagebox.showerror(title = 'Error', message = 'Invalid Rate!')
        elif len(distance) == 0:
            messagebox.showerror(title = 'Error', message = 'Enter Distance!') 
        elif (any((not(y.isdigit() or '.' in y)) for y in distance)) or distance.count('.')>1:
            messagebox.showerror(title = 'Error', message = 'Invalid Distance!')
        else:
            rate = float(self.ent_RperMile.get())
            distance = float(self.ent_Tdistance.get())
            total_price = rate * distance
            self.ent_Tprice.config(state=NORMAL)
            self.T_Price.set(str(round(total_price,2)))
            self.ent_Tprice.config(state=DISABLED)
