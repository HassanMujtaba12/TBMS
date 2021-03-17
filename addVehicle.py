from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
import mysql.connector


class AddVehicle():
    def __init__(self, master,mydb):
        self.mycursor = mydb.cursor()
        def update(rows):
            self.query_box.delete(*self.query_box.get_children())
            for i in rows:
                self.query_box.insert('','end', values=i)
        
        def search():
            self.mycursor = mydb.cursor()
            query = "SElECT Reg_No, Make, Model, DriverID  From vehicle WHERE Reg_No LIKE '%"+self.ent_Search.get()+"%' OR DriverID LIKE '%"+self.ent_Search.get()+"%'"
            self.mycursor.execute(query)
            rows=self.mycursor.fetchall()
            update(rows)
            
        def clear():
            self.mycursor = mydb.cursor()
            query = "SElECT Reg_No, Make, Model, DriverID  From vehicle"
            self.mycursor.execute(query)
            rows=self.mycursor.fetchall()
            update(rows)
        def get_row(event):
            self.mycursor = mydb.cursor()
            rowid = self.query_box.identify_row(event.y)
            item=self.query_box.item(self.query_box.focus())
            query = "SELECT * FROM vehicle WHERE Reg_No = '"+str(item['values'][0])+"'"
            self.mycursor.execute(query)
            items = list(self.mycursor.fetchall()[0])
            self.RegNo.set(items[0])
            self.Make.set(items[1])
            self.Model.set(items[2])
            self.Colour.set(items[3])
            self.PCO.set(items[4])
            self.ent_VPCOExp_date.set_date(items[5])
            self.ent_MOT_Exp_date.set_date(items[6])
            self.ent_driverID.current(self.just_ids.index(items[7])+1)
            
            
        def test():
            print(self.ent_driver.get())
            
        def update_vehicle():
            self.mycursor = mydb.cursor()
            pco_date = self.ent_VPCOExp_date.get()
            MOT_date = self.ent_MOT_Exp_date.get()

            dID = self.ent_driverID.get()
            if messagebox.askyesno("Confirm Please", "Are you sure you want to update this vehicle?"):
                query = """UPDATE vehicle SET Make = %s, Model= %s, Colour= %s, PCO_No= %s,
                PCO_Exp= %s, MOT_Exp= %s, DriverID= %s WHERE Reg_No = %s"""
                self.mycursor.execute(query, (self.Make.get(), self.Model.get(), self.Colour.get(), self.PCO.get(),
                                              pco_date, MOT_date, dID[0:dID.index('-')], self.RegNo.get()))
                mydb.commit()
                self.mycursor.close()
                clear()
            else:
                return True
        def add_new():
            pco_date = self.ent_VPCOExp_date.get()
            MOT_date = self.ent_MOT_Exp_date.get()
            self.mycursor = mydb.cursor()
            query = """INSERT INTO vehicle VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
            self.mycursor.execute(query, (self.RegNo.get(), self.Make.get(), self.Model.get(), self.Colour.get(), self.PCO.get(),
                                          pco_date, MOT_date,self.ent_driverID.get()[0:self.ent_driverID.get().index('-')]))
            mydb.commit()
            self.mycursor.close()
            clear()
        def delete_vehicle():
            self.mycursor = mydb.cursor()
            vehicle = self.RegNo.get()
            if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this Vehicle?"):
                query = "DELETE FROM vehicle WHERE Reg_No = "+Reg_No
                self.mycursor.execute(query)
                mydb.commit()
                self.mycursor.close()
                clear()
            else:
                return True        
        
        def refresh():
            self.options=['Select Driver']
            self.just_ids = []
            self.mycursor = mydb.cursor()
            q="Select Driver_ID, Firstname from driver"
            self.mycursor.execute(q)
            self.ids=self.mycursor.fetchall()
            mydb.commit()
            self.mycursor.close()
            for i in self.ids:
                self.just_ids.append(i[0])
                self.options.append(str(i[0]) +'-'+i[1])
            self.ent_driverID['values'] = self.options     
            self.RegNo.set('')
            self.Make.set('')
            self.Model.set('')
            self.Colour.set('')
            self.PCO.set('')
            self.ent_driverID.current(0)
        def vehicle_validation(func):
            make = self.ent_VMake.get()
            model = self.ent_VModel.get()
            colour = self.ent_Vcolour.get()
            pco_no = self.ent_VPCO.get()
            driver = self.ent_driverID.get()
            Regno = self.ent_VReg.get()

            if (any(not(x.isalpha()) for x in make)):
                messagebox.showerror(title = 'Error', message = 'Make contains invalid characters!')
            elif (any(not(x.isalpha()) for x in colour)):
                messagebox.showerror(title = 'Error', message = 'Colour contains invalid characters!')
            elif len(Regno) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter PCO No!')    
            elif len(make) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Firstname!')
            elif len(model) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Lastname!')
            elif len(colour) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter Lastname!')
            elif len(pco_no) == 0:
                messagebox.showerror(title = 'Error', message = 'Enter PCO No!')
            elif driver == 'Select Driver':
                messagebox.showerror(title = 'Error', message = 'Driver is not selected!')
            else:
                if func == 'add':
                    add_new()
                elif func == 'update':
                    update_vehicle()
                elif func == 'delete':
                    delete_vehicle()
        def add_vehicle():
            vehicle_validation('add')
        def del_vehicle():
            vehicle_validation('delete')
        def upd_vehicle():
            vehicle_validation('update')
        
        
        
        self.mainFrame = Frame(master, width=950, background = 'yellow')
        self.mainFrame.pack(fill=Y, expand=True)
        self.topFrame = Frame(self.mainFrame,width = 950, height=100, background="blue")
        self.topFrame.pack(fill=X, expand=True, side=TOP)
        #self.bottomFrame = Frame(master ,width=950, height=700, background = 'blue')
        #self.bottomFrame.pack(fill=None, expand=True)
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
                                 columns=('Reg No','Car Make','Model', 'Driver ID'),height=25,yscrollcommand=query_scroll.set)
        self.query_box["columns"] = ('Reg No','Car Make','Model','Driver ID')
        self.query_box.grid(row=0, column=0)
        self.query_box.column("Reg No", width=100, anchor="center")
        self.query_box.heading("Reg No", text="Reg No")        
        self.query_box.column("Car Make", width=100, anchor="center")
        self.query_box.heading("Car Make", text="Car Make")
        self.query_box.column("Model", width=150, anchor="center")
        self.query_box.heading("Model", text="Model")
        self.query_box.column('Driver ID', width=100, anchor="center")
        self.query_box.heading('Driver ID', text='Driver ID')
        self.query_box["show"] = "headings"
        
        self.query_box.bind('<Double 1>', get_row)
        
        self.mycursor = mydb.cursor()
        query = "SElECT Reg_No, Make, Model, DriverID  From vehicle"
        self.mycursor.execute(query)
        rows = self.mycursor.fetchall()
        update(rows)
        

##################### Widgets ########################################################
        #Search Bar
        self.search_query=StringVar()
        self.lbl_Search = Label(self.topFrame, text = 'Search: ', font='arial 12 bold', fg='white', bg='blue')
        self.lbl_Search.place(x=40, y=20)
        self.ent_Search = Entry(self.topFrame,width=30, bd=4, textvariable=self.search_query)
        self.ent_Search.place(x=150, y=20)
        
        self.search_btn = Button(self.topFrame, text= 'Search', width=6, command=search)
        self.search_btn.place(x=150, y=60)
        
        self.clr_btn = Button(self.topFrame, text= 'Clear',width=6,command=clear)
        self.clr_btn.place(x=250, y=60)
        
        #Refresh Label
        self.rfr_btn = Button(self.formFrame, text= 'Refresh and Clear', command=refresh)
        self.rfr_btn.place(x=330, y=10)
        
        
        # Reg No
        self.RegNo = StringVar()
        self.lbl_VReg = Label(self.formFrame, text='Reg No: ', font='arial 12 bold', fg='white',bg='#fcc324')
        self.lbl_VReg.place(x=40, y=40)
        self.ent_VReg = Entry(self.formFrame, width=30, bd=4, textvariable = self.RegNo)
        self.ent_VReg.place(x=150, y=45)
        
        # Vehicle Make
        self.Make = StringVar()
        self.lbl_VMake = Label(self.formFrame, text='Make :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_VMake.place(x=40, y=80)
        self.ent_VMake = Entry(self.formFrame, width=30, bd=4, textvariable = self.Make)
        self.ent_VMake.place(x=150, y=85)

        # Vehicle Model
        self.Model = StringVar()
        self.lbl_VModel = Label(self.formFrame, text='Model :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_VModel.place(x=40, y=120)
        self.ent_VModel = Entry(self.formFrame, width=30, bd=4, textvariable = self.Model)
        self.ent_VModel.place(x=150, y=125)

        # Vehicle Colour
        self.Colour = StringVar()
        self.lbl_Vcolour = Label(self.formFrame, text='Colour :', font='arial 12 bold', fg='white', bg='#fcc324')
        self.lbl_Vcolour.place(x=40, y=160)
        self.ent_Vcolour = Entry(self.formFrame, width=30, bd=4, textvariable = self.Colour)
        self.ent_Vcolour.place(x=150, y=165)

        # Vehicle PCO Licence No
        self.PCO = StringVar()
        self.lbl_VPCO=Label(self.formFrame,text='PCO No :',font='arial 12 bold',fg='white',bg='#fcc324')
        self.lbl_VPCO.place(x=40,y=200)
        self.ent_VPCO=Entry(self.formFrame,width=30,bd=4, textvariable = self.PCO)
        self.ent_VPCO.place(x=150,y=205)     
        
        #Vehicle PCO Expiry
        self.lbl_VPCOExp_date = Label(self.formFrame, text='PCO Exp :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_VPCOExp_date.place(x=40, y=240)
        self.ent_VPCOExp_date = DateEntry(self.formFrame, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, year=2020, date_pattern='y-mm-dd')
        self.ent_VPCOExp_date.place(x=150, y=245)

        #Vehicle MOT Expiry
        self.lbl_MOT_Exp_date = Label(self.formFrame, text='MOT Exp :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
        self.lbl_MOT_Exp_date.place(x=40, y=280)
        self.ent_MOT_Exp_date = DateEntry(self.formFrame, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, year=2020, date_pattern='y-mm-dd')
        self.ent_MOT_Exp_date.place(x=150, y=285)
        
        # Driver ID
        
        self.lbl_driverID = Label(self.formFrame, text='Driver ID:', font='arial 12 bold', fg='white', bg='#fcc324',width=11,anchor=W)
        self.lbl_driverID.place(x=40, y=320)
        self.ent_driverID = ttk.Combobox(self.formFrame,width=28, state='readonly',values=['Select Driver'])
        refresh()
        self.ent_driverID.place(x=150,y=325)
        self.ent_driverID.current(0)
        

        #Add Button
        self.add_button=Button(self.formFrame,text='Add Vehicle', width =11, command = add_vehicle)
        self.add_button.place(x=40,y=470)
        
        #Update Button
        self.upd_button=Button(self.formFrame,text='Update Vehicle',width=11, command = upd_vehicle)
        self.upd_button.place(x=170,y=470)
        
        #Delete Button
        self.del_button=Button(self.formFrame,text='Delete Vehicle',width=11, command = del_vehicle)
        self.del_button.place(x=300,y=470)
        


