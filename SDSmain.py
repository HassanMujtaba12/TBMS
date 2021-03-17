from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import addBooking, addClient, addDriver, addVehicle, report, Alerts
import mysql.connector

# Connecting to the cloud Mysql Server
mydb = mysql.connector.connect(
    host="b6hew5akkes3sw8ge670-mysql.services.clever-cloud.com",
    user="ueytj9f39lqmpco8",
    passwd="eLbRuhfAsFDSbgJ4810N",
    database = "b6hew5akkes3sw8ge670"
)
class Main(object):
    def __init__(self,master):
        self.master = master
        #Creating the GUI for the user
        self.master.configure(bg='white')
        self.master.option_add('*Font', 'Goergia 11') #font for all widgets
        self.master.option_add('*Background', 'ivory2')#background of all widgets
        self.master.option_add('*Label.Font', 'Arial 12') #font for all labels
        self.master.geometry("1350x714+20+20")
        self.master.resizable(False,False)

        self.mainFrame=Frame(self.master)
        self.mainFrame.pack()
        #top frames
        self.topFrame= Frame(self.mainFrame,width=1020,height=700,bg='#f8f8f8',
                             padx=5,relief=SUNKEN,borderwidth=1)
        self.topFrame.pack(side=TOP,fill='both', expand = True)
##############################################################################################################################
        self.tabs= ttk.Notebook(self.topFrame,width=1350,height=750)
        ttk.Style().configure('Tab', foreground='black', background='blue')
        self.tabs.pack(expand=True)
        self.book_icon=PhotoImage(file='icons/book.gif')
        self.manage_icon=PhotoImage(file='icons/management.gif')
        self.alert_icon=PhotoImage(file='icons/Alert.gif')
        
        self.book=ttk.Frame(self.tabs)
        self.drVeh_tab=ttk.Frame(self.tabs)
        self.report_tab=ttk.Frame(self.tabs)
        self.alert_tab = ttk.Frame(self.tabs)
        
        self.tabs.add(self.book,text='Booking',image=self.book_icon,compound=LEFT)
        self.tabs.add(self.drVeh_tab,text='Management',image=self.manage_icon,compound=LEFT)
        self.tabs.add(self.report_tab,text='Reports',image=self.book_icon,compound=LEFT)
        self.tabs.add(self.alert_tab,text='Alerts',image=self.alert_icon,compound=LEFT)
        
        #Driver and Vehicle tabs
        self.DV = ttk.Notebook(self.drVeh_tab, width=1350, height=750)
        self.DV.pack()
        self.driver = ttk.Frame(self.DV)
        self.vehicle = ttk.Frame(self.DV)
        self.client = ttk.Frame(self.DV)
        self.DV.add(self.driver, text='Driver', compound=LEFT)
        self.DV.add(self.vehicle, text='Vehicle', compound=LEFT)
        self.DV.add(self.client, text='Client', compound=LEFT)
        
        addBooking.AddBooking(self.book,mydb)
        addDriver.AddDriver(self.driver,mydb)
        addVehicle.AddVehicle(self.vehicle,mydb)
        addClient.AddClient(self.client,mydb)
        report.Report(self.report_tab,mydb)
        Alerts.Alert(self.alert_tab, mydb)
root = Tk()
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        mydb.close()
        root.destroy()
    else:
        pass
def main():
    app = Main(root)
    root.title("Skylink Dispatch System")
    #root.geometry("1350x750+350+200")
    root.iconbitmap('icons/Skylink.ico')
    root.protocol("WM_DELETE_WINDOW",on_closing)
    root.mainloop()

if __name__ == '__main__':
    main()
