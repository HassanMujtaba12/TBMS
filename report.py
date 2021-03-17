from tkinter import *
import pandas as pd
from tkinter import ttk
from tkinter import filedialog
import mysql.connector
from tkcalendar import Calendar, DateEntry


class Report():
        def __init__(self,master,mydb):
            self.main = master
            def adding_to_list(lt, var,var_check):
                if var_check.get() == var['onvalue']:
                    lt.append(var_check.get())
                else:
                    return True
            def crefresh_filter():
                #Client Add
                self.client_options = ['All Clients']
                self.client_ids = []
                self.mycursor=mydb.cursor()
                query = "Select Client_ID, Name, Phone from client"
                self.mycursor.execute(query)
                self.myids = self.mycursor.fetchall()
                for client in self.myids:
                    self.client_ids.append(client[0])
                    self.client_options.append(str(client[0]) + ' - '+client[1]+'('+client[2]+')')
                self.ent_clientID['values'] = self.client_options
            def drefresh_filter():
                self.options=['All Drivers']
                self.just_ids = []
                self.mycursor = mydb.cursor()
                q="Select Driver_ID, Firstname from driver"
                self.mycursor.execute(q)
                self.ids=self.mycursor.fetchall()
                self.mycursor.close()
                for i in self.ids:
                    self.just_ids.append(i[0])
                    self.options.append(str(i[0]) +'-'+i[1])
                self.ent_driverID['values'] = self.options
            def removing():
                self.displayFrame.destroy()
                self.displayFrame = Frame(self.main,bg='grey')
                self.displayFrame.pack(fill='both') 
                self.optionsFrame = Frame(self.displayFrame, height=200, bg='white')
                self.optionsFrame.pack(fill=X, side=TOP)

                
                # Style configurations for ttk       
                style = ttk.Style()
                style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
                style.configure("Treeview", font=("Segoe UI", 10))
            def update(trv,rows):
                trv.delete(*trv.get_children())
                for i in rows:
                    trv.insert('','end', values=i)
            def client():
                removing()    
                self.clt_var=StringVar()
                self.clt_check = Checkbutton(self.optionsFrame, text = 'ClientID',onvalue ='booking.Client_ID',
                                      offvalue = '', height=2,width = 10,variable = self.clt_var)
                self.clt_check.place(x=150,y=10)
                self.clt_check.select()     
                self.cname_var=StringVar()
                self.cname_check = Checkbutton(self.optionsFrame, text = "Name",onvalue ='client.Name',
                                      offvalue = '', height=2,width = 10,variable = self.cname_var)
                self.cname_check.place(x=300,y=10)
                self.cname_check.select() 
                self.cphone_var=StringVar()
                self.cphone_check = Checkbutton(self.optionsFrame, text = "Phone",onvalue ='client.Phone',
                                      offvalue = '', height=2,width = 10,variable = self.cphone_var)
                self.cphone_check.place(x=450,y=10)
                self.cphone_check.select()      
                self.cemail_var=StringVar()
                self.cemail_check = Checkbutton(self.optionsFrame, text = "Email",onvalue ='client.Email',
                                      offvalue = '', height=2,width = 10,variable = self.cemail_var)
                self.cemail_check.place(x=600,y=10)
                self.cemail_check.select()
                self.cdate_var=StringVar()
                self.cdate_check = Checkbutton(self.optionsFrame, text = "Date",onvalue ='booking.Job_Date',
                                      offvalue = '', height=2,width = 10,variable = self.cdate_var)
                self.cdate_check.place(x=750,y=10)
                self.cdate_check.select()  
                self.ctime_var=StringVar()
                self.ctime_check = Checkbutton(self.optionsFrame, text = "Time",onvalue ='booking.Time',
                                      offvalue = '', height=2,width = 10,variable = self.ctime_var)
                self.ctime_check.place(x=900,y=10)
                self.ctime_check.select()
                self.cpick_var=StringVar()
                self.cpick_check = Checkbutton(self.optionsFrame, text = "Pick-Up",onvalue ='booking.Pick_Up_Address',
                                      offvalue = '', height=2,width = 10,variable = self.cpick_var)
                self.cpick_check.place(x=1050,y=10)
                self.cpick_check.select()
                self.cdrop_var=StringVar()
                self.cdrop_check = Checkbutton(self.optionsFrame, text = "Drop-off",onvalue ='booking.Drop_Off_Address',
                                      offvalue = '', height=2,width = 10,variable = self.cdrop_var)
                self.cdrop_check.place(x=1200,y=10)
                self.cdrop_check.select()
                
                self.lbl_clientID = Label(self.optionsFrame, text='Client ID:', font='arial 12 bold', fg='white', bg='#fcc324',width=11,anchor=W)
                self.lbl_clientID.place(x=900, y=60)
                self.ent_clientID = ttk.Combobox(self.optionsFrame,width=28, state='readonly')
                self.ent_clientID['values'] = ['All']
                crefresh_filter()
                self.ent_clientID.place(x=1050,y=60)
                self.ent_clientID.current(0)
                
                #From Date
                self.clbl_from_date = Label(self.optionsFrame, text='From :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
                self.clbl_from_date.place(x=900, y=110)
                self.cent_from_date = DateEntry(self.optionsFrame, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, year=2019, date_pattern='y-mm-dd')
                self.cent_from_date.place(x=1050, y=110)
                
                #To Date
                self.clbl_to_date = Label(self.optionsFrame, text='To :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
                self.clbl_to_date.place(x=900, y=160)
                self.cent_to_date = DateEntry(self.optionsFrame, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, year=2021, date_pattern='y-mm-dd')
                self.cent_to_date.place(x=1050, y=160)
                

                self.showbtn = Button(self.optionsFrame, text='SHOW',command= client_show)
                self.showbtn.place(x=300, y=100)
                
            def driver():
                removing()
                self.drv_var=StringVar()
                self.drv_check = Checkbutton(self.optionsFrame, text = 'DriverID',onvalue ='booking.Driver_ID',
                                      offvalue = '', height=2,width = 10,variable = self.drv_var)
                self.drv_check.place(x=150,y=10)
                self.drv_check.select()     
                self.dname_var=StringVar()
                self.dname_check = Checkbutton(self.optionsFrame, text = "Name",onvalue ='driver.Firstname',
                                      offvalue = '', height=2,width = 10,variable = self.dname_var)
                self.dname_check.place(x=300,y=10)
                self.dname_check.select() 
                self.dprice_var=StringVar()
                self.dprice_check = Checkbutton(self.optionsFrame, text = "Price",onvalue ='booking.Price',
                                      offvalue = '', height=2,width = 10,variable = self.dprice_var)
                self.dprice_check.place(x=450,y=10)
                self.dprice_check.select() 
                self.demail_var=StringVar()
                self.demail_check = Checkbutton(self.optionsFrame, text = "Email",onvalue ='driver.Email',
                                      offvalue = '', height=2,width = 10,variable = self.demail_var)
                self.demail_check.place(x=600,y=10)
                self.demail_check.select()
                self.ddate_var=StringVar()
                self.ddate_check = Checkbutton(self.optionsFrame, text = "Date",onvalue ='booking.Job_Date',
                                      offvalue = '', height=2,width = 10,variable = self.ddate_var)
                self.ddate_check.place(x=750,y=10)
                self.ddate_check.select()  
                self.dtime_var=StringVar()
                self.dtime_check = Checkbutton(self.optionsFrame, text = "Time",onvalue ='booking.Time',
                                      offvalue = '', height=2,width = 10,variable = self.dtime_var)
                self.dtime_check.place(x=900,y=10)
                self.dtime_check.select()
                self.dpick_var=StringVar()
                self.dpick_check = Checkbutton(self.optionsFrame, text = "Pick-Up",onvalue ='booking.Pick_Up_Address',
                                      offvalue = '', height=2,width = 10,variable = self.dpick_var)
                self.dpick_check.place(x=1050,y=10)
                self.dpick_check.select()
                self.ddrop_var=StringVar()
                self.ddrop_check = Checkbutton(self.optionsFrame, text = "Drop-off",onvalue ='booking.Drop_Off_Address',
                                      offvalue = '', height=2,width = 10,variable = self.ddrop_var)
                self.ddrop_check.place(x=1200,y=10)
                self.ddrop_check.select()
                
                self.lbl_driverID = Label(self.optionsFrame, text='Driver ID:', font='arial 12 bold', fg='white', bg='#fcc324',width=11,anchor=W)
                self.lbl_driverID.place(x=900, y=60)
                self.ent_driverID = ttk.Combobox(self.optionsFrame,width=28, state='readonly',values=['All Drivers'])
                self.ent_driverID['values'] = ['All']
                drefresh_filter()
                self.ent_driverID.place(x=1050,y=60)
                self.ent_driverID.current(0)
                
                #From Date
                self.dlbl_from_date = Label(self.optionsFrame, text='From :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
                self.dlbl_from_date.place(x=900, y=110)
                self.dent_from_date = DateEntry(self.optionsFrame, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, year=2019, date_pattern='y-mm-dd')
                self.dent_from_date.place(x=1050, y=110)
                
                #To Date
                self.dlbl_to_date = Label(self.optionsFrame, text='To :', font='arial 12 bold', fg='white', bg='#fcc324',width = 11,anchor = W)
                self.dlbl_to_date.place(x=900, y=160)
                self.dent_to_date = DateEntry(self.optionsFrame, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, year=2021, date_pattern='y-mm-dd')
                self.dent_to_date.place(x=1050, y=160)
                self.showbtn_drv = Button(self.optionsFrame, text='SHOW',command= driver_show)
                self.showbtn_drv.place(x=300, y=100)
            
            def driver_show():
                master = Tk() 
                master.configure(bg='white')
                master.option_add('*Font', 'Goergia 12') #font for all widgets
                master.option_add('*Background', 'ivory2')#background of all widgets
                master.option_add('*Label.Font', 'helvetica 14') #font for all labels
                master.geometry("1000x750+200+50")
                master.title("Driver Report")
                master.resizable(False,False)
                query_scroll = Scrollbar(master)
                query_box = ttk.Treeview(master,height=20,yscrollcommand=query_scroll.set)
                cols_drv =[]
                myVars_drv = [self.drv_check, self.dname_check, self.dprice_check,self.demail_check,
                              self.ddate_check,self.dtime_check,self.dpick_check,self.ddrop_check]
                myCheckVars_drv = [self.drv_var, self.dname_var, self.dprice_var, self.demail_var,
                                   self.ddate_var,self.dtime_var,self.dpick_var,self.ddrop_var]
                for f in range(0,len(myVars_drv)):
                    adding_to_list(cols_drv, myVars_drv[f], myCheckVars_drv[f])
                query_col_name_drv =[]
                for j in range(1,len(cols_drv)+1):
                    query_col_name_drv.append(j)
                query_box["columns"] = tuple(query_col_name_drv)
                query_columns_drv = query_box['columns']
                query_box.grid(row=0, column=0)
                query_scroll.grid(row=0, column=1, sticky="nsew", rowspan=2)
                df_columns= []
                for i in range(0,len(query_columns_drv)):     
                    query_box.column(query_columns_drv[i], width=100, anchor="center")
                    query_box.heading(query_columns_drv[i], text=cols_drv[i].split('.')[1])
                    df_columns.append(cols_drv[i].split('.')[1])
                query_box["show"] = "headings"
                self.mycursor = mydb.cursor()
                db_cols_drv =[]
                
                for k in query_col_name_drv:
                    db_cols_drv.append(str(cols_drv[k-1]))
                
                driverid = self.ent_driverID.get()
                #print(driverid)
                dl = ""
                if driverid == 'All Drivers':
                    dl='driver.Driver_ID'
                else:
                    dl = driverid[0:driverid.index('-')]
                job_from_date = self.dent_from_date.get()
                job_to_date = self.dent_to_date.get()
                query = f"""select {','.join(db_cols_drv)}
                from booking Join driver on booking.Driver_ID = driver.Driver_ID Where (booking.Job_Date>= '{job_from_date}' AND booking.Job_Date<= '{job_to_date}') AND driver.Driver_ID = {dl}"""
                self.mycursor.execute(query)
                row=self.mycursor.fetchall()
                
                def exportCSV():
                    df = pd.DataFrame(row, columns = df_columns)
                    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
                    df.to_csv(export_file_path, index = False, header=True)
                    #df.to_html(export_file_path)
                    
                
                saveAsButton_CSV = Button(master,text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
                saveAsButton_CSV.grid(row=0, column=3)
                update(query_box,row)

                
            def client_show():   
                master = Tk() 
                
                master.configure(bg='white')
                master.option_add('*Font', 'Goergia 12') #font for all widgets
                master.option_add('*Background', 'ivory2')#background of all widgets
                master.option_add('*Label.Font', 'helvetica 14') #font for all labels
                master.geometry("1100x750+200+50")
                master.title("Client Report")
                master.resizable(False,False)
                query_scroll = Scrollbar(master)
                query_box = ttk.Treeview(master,height=20,yscrollcommand=query_scroll.set)
                cols_clt =[]
                myVars_clt = [self.clt_check, self.cname_check, self.cphone_check, self.cemail_check,
                              self.cdate_check,self.ctime_check,self.cpick_check,self.cdrop_check]
                myCheckVars_clt = [self.clt_var, self.cname_var, self.cphone_var, self.cemail_var,
                                   self.cdate_var,self.ctime_var,self.cpick_var,self.cdrop_var]
                size_dict = {'Client_ID':70, 'Name':80,'Phone':80,'Email':160,'Job_Date':80,'Time':80,'Pick_Up_Address':200,'Drop_Off_Address':200}
                for f in range(0,len(myVars_clt)):
                    adding_to_list(cols_clt, myVars_clt[f], myCheckVars_clt[f])
                query_col_name_clt =[]
                for j in range(1,len(cols_clt)+1):
                    query_col_name_clt.append(j)
                query_box["columns"] = query_col_name_clt
                query_columns_clt = query_box['columns']

                query_box.grid(row=0, column=0)
                query_scroll.grid(row=0, column=1, sticky="nsew", rowspan=2)
                df_columns =[]
                for i in range(0,len(query_columns_clt)):
                    query_box.column(query_columns_clt[i],width=size_dict[cols_clt[i].split('.')[1]], stretch=YES, anchor="center")
                    query_box.heading(query_columns_clt[i], text=cols_clt[i].split('.')[1])  
                    df_columns.append(cols_clt[i].split('.')[1])
                query_box["show"] = "headings"
                self.mycursor = mydb.cursor()
                db_cols_clt =[]
                for k in query_col_name_clt:
                    db_cols_clt.append(str(cols_clt[k-1]))
                clientid = self.ent_clientID.get()
                #print(clientid)
                cl = ""
                if clientid == 'All Clients':
                    cl='client.Client_ID'
                else:
                    cl = clientid[0:clientid.index('-')]
                job_from_date = self.cent_from_date.get()
                job_to_date = self.cent_to_date.get()
                self.mycursor = mydb.cursor()
                query = f"""select {','.join(db_cols_clt)} from booking
                Join client on booking.Client_ID = client.Client_ID Where (booking.Job_Date>= '{job_from_date}' AND booking.Job_Date<= '{job_to_date}') AND client.Client_ID = {cl}"""
                self.mycursor.execute(query)
                row=self.mycursor.fetchall()

                def exportCSV():
                    df = pd.DataFrame(row, columns = df_columns)
                    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
                    df.to_csv(export_file_path, index = False, header=True)
                    #df.to_html(export_file_path)
                    
                
                saveAsButton_CSV = Button(master,text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
                saveAsButton_CSV.grid(row=0, column=3)
                update(query_box,row)
                
            self.reportFrm = Frame(self.main, height=40, bg='yellow')
            self.reportFrm.pack(side=TOP,fill=X)
            self.reportLabel= Label(self.reportFrm, text= 'Reports', font = ('arial 14 bold'))
            self.reportLabel.place(x=600, y=5)

            self.btnFrame = Frame(self.main, height=50,bg='blue')
            self.btnFrame.pack(fill=X, side=TOP)
            self.displayFrame = Frame(self.main,bg='grey')
            self.displayFrame.pack(fill='both') 
            self.optionsFrame = Frame(self.displayFrame, height=200, bg='white')
            self.optionsFrame.pack(fill=X, side=TOP)
   
            btn_client = Button(self.btnFrame, text='Client',command=client)
            btn_client.place(x=100, y=5)
            
            btn_driver = Button(self.btnFrame, text='Driver',command=driver)
            btn_driver.place(x=400, y=5)
            
