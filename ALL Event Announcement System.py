from tkinter import *
import sqlite3
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from io import BytesIO
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
from datetime import date 
import time
from threading import *
from tkcalendar import Calendar

def raise_frame(frame):
    frame.tkraise()
    
root = Tk()
root.geometry('925x500+200+100')
root.resizable(0,0)
root.title('School event announcement')


Reminder = Frame(root)
Chatbox = Frame(root)
l = Frame(root)
w = Frame(root)

#################################################### String Variable ############################################################
nameinput = StringVar()
emailinput = StringVar()

########################################## Add school event (admin) ##################################################################

code=StringVar()
eventtitle=StringVar()
date1=StringVar()
time1=StringVar()
venue1=StringVar() 

def upload_image():
    global filename,img
    f_types=[('Png files','*.png'),('Jpg files','*.jpg')]
    filename=filedialog.askopenfilename(filetypes=f_types)
    if(filename):
        img=Image.open(filename)
        img = img.resize((190,220))
        img = ImageTk.PhotoImage(img)
        label=Label(add_eventframe, image=img, width=190, height=220)
        label.place(x=650,y=150)   
   
def submit():

    if eventtitle.get() =='' or date1.get() =='' or time1.get()=='' or venue1.get()=='':
        messagebox.showerror("Error", "Please complete the required field!")
    else:
        try:
          fb=open(filename,'rb')   
          fb=fb.read()
          db=sqlite3.connect('userinfo.sqlite')
          cursor = db.cursor()
          cursor.execute("""CREATE TABLE IF NOT EXISTS schoolevent(event_code VARCHAR NOT NULL PRIMARY KEY,
                          event_name VARCHAR (100) NOT NULL UNIQUE, date VARCHAR (12)  NOT NULL, time VARCHAR (20)  NOT NULL, 
                          venue VARCHAR (100) NOT NULL, image BLOB)""")
          cursor.execute("INSERT INTO schoolevent(event_code, event_name, date, time, venue, image) VALUES(?,?,?,?,?,?)",
                         (code.get(), eventtitle.get(), date1.get(), time1.get(), venue1.get(), fb))
          db.commit()
          db.close()
          
          messagebox.showinfo("Info","An School Event has been successfully created.")
        except:
          messagebox.showerror('Error', 'Event is not created, please try again!')


add_eventframe = Frame(root, width=925, height=500, bg='#FCE1F3')
add_eventframe.place(x=0,y=0)
addNew = Label(add_eventframe, text='Add New School Events', fg="Hotpink2",bg="#FCE1F3",font=("Time New Roman",26,"bold")).place(x=290,y=54)


code_label = Label(add_eventframe, text='Event Code:', bg='#FCE1F3', font=('Times New Roman bold', 13)).place(x=200,y=150)
title_label = Label(add_eventframe, text='School Event:', bg='#FCE1F3', font=('Times New Roman bold', 13)).place(x=200,y=200)
date_label = Label(add_eventframe, text='Date:', bg='#FCE1F3', font=('Times New Roman bold', 13)).place(x=200,y=250)
time_label = Label(add_eventframe, text='Time:', bg='#FCE1F3', font=('Times New Roman bold', 13)).place(x=200,y=300)
venuee = Label(add_eventframe, text='Venue', bg='#FCE1F3', font=('Times New Roman bold', 13)).place(x=200,y=350)

im = LabelFrame(add_eventframe, bg='white', width=190, height=220).place(x=650,y=150)

code_entry =Entry(add_eventframe, width=40,textvariable=code).place(x=325,y=150)
title_entry = Entry(add_eventframe,width=40,textvariable=eventtitle).place(x=325,y=200)
date = DateEntry(add_eventframe, width=40, textvariable=date1).place(x=325,y=250)
time = Entry(add_eventframe, width=40,textvariable=time1).place(x=325,y=300)
venue = Entry(add_eventframe, width=40,textvariable=venue1).place(x=325, y=350)

Create_new=Button(add_eventframe,text='Create New', bg="#F5FFFA",fg="black",border=0,font=('Times New Roman bold', 13), command=submit).place(x=400,y=420)
uploadImage_button=Button(add_eventframe, text='Upload Image', bg="#F5FFFA",fg="black",border=0,font=('Times New Roman bold', 13), command=upload_image).place(x=685,y=420)


################################################# Manage Event Admin #########################################################################

def manageeventadmin():

    manageeventframe = Frame(root, width = 1000, height = 700, bg='#FCE1F3')
    manageeventframe.place(x=0,y=0)

    manageeventtitle = Label(manageeventframe, text="Manage School Events", fg="Hotpink2",bg="#FCE1F3",font=("Time New Roman",26,"bold")).place(x=290,y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview", bg = "#D3D3D3", fg = "black", rowheight = 20, fieldbackground = "#D3D3D3")
    style.map("Treeview", bg =[('selected', "#347083")])

    thetreeframe = Frame(manageeventframe)
    thetreeframe.pack(padx=1,pady=275)

    treescroll = Scrollbar(thetreeframe)
    treescroll.pack(side = RIGHT, fill = Y)

    manage_tree = ttk.Treeview(thetreeframe, yscrollcommand=treescroll.set, selectmode="extended")
    manage_tree.pack()

    treescroll.config(command=manage_tree.yview)

    manage_tree['column'] = ('1','2','3','4','5','6')
    manage_tree['show'] = 'headings'

    manage_tree.column('1', width = 70, anchor = 'c')
    manage_tree.column('2', width = 300, anchor = 'c')
    manage_tree.column('3', width = 80, anchor = 'c')
    manage_tree.column('4', width = 120, anchor = 'c')
    manage_tree.column('5', width = 300, anchor = 'c')
    manage_tree.column('6', width = 1, anchor = 'c')

    manage_tree.heading('1', text = 'Event Code')
    manage_tree.heading('2', text = 'Event Name')
    manage_tree.heading('3', text = 'Date')
    manage_tree.heading('4', text = 'Time')
    manage_tree.heading('5', text = 'Venue')


    manage_tree.tag_configure('odd', background="white")
    manage_tree.tag_configure('even', background="lightblue")

    db=sqlite3.connect('userinfo.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM schoolevent")
    displayrecord = cursor.fetchall()

    global count 
    count = 0
    for all in displayrecord: 
        if count % 2 == 0:  
            manage_tree.insert('', 'end', iid = count, values = (all[0], all[1], all[2],all[3], all[4]), tags=('even',))
        else:
            manage_tree.insert('', 'end', iid = count, values = (all[0], all[1], all[2],all[3], all[4]), tags=('odd',))
        count += 1

    entryframe = LabelFrame(manageeventframe, text = "Manage School Event")
    entryframe.place(x=3,y=50)

    eventcodemanage = Label(entryframe, text= "Event Code")
    eventcodemanage.grid(row=0, column=0, padx=10, pady=10)
    eventcodeentry = Entry(entryframe, width=100)
    eventcodeentry.grid(row=0, column=1, padx=10, pady=10)

    eventnamemanage = Label(entryframe, text= "Event Name")
    eventnamemanage.grid(row=1, column=0, padx=10, pady=10)
    eventnameentry = Entry(entryframe, width=100)
    eventnameentry.grid(row=1, column=1, padx=10, pady=10)

    eventdatemanage = Label(entryframe, text= "Event Date")
    eventdatemanage.grid(row=2, column=0, padx=10, pady=10)
    eventdateentry = Entry(entryframe, width=100)
    eventdateentry.grid(row=2, column=1, padx=10, pady=10)

    eventtimemanage = Label(entryframe, text= "Event Time")
    eventtimemanage.grid(row=3, column=0, padx=10, pady=10)
    eventtimeentry = Entry(entryframe, width=100)
    eventtimeentry.grid(row=3, column=1, padx=10, pady=10)

    eventvenuemanage = Label(entryframe, text= "Event Venue")
    eventvenuemanage.grid(row=4, column=0, padx=10, pady=10)
    eventvenueentry = Entry(entryframe, width=100)
    eventvenueentry.grid(row=4, column=1, padx=10, pady=10)

    def update_data():
        if eventcodeentry.get() == "" or eventnameentry.get() == "" or eventdateentry.get() == "" or eventtimeentry.get() == "" or eventvenueentry.get() == "" :
            messagebox.showerror("Error","Please do not leave any event details blank !")  
        else:    
            select = manage_tree.focus()
            manage_tree.item(select, text="", values=(eventcodeentry.get(),eventnameentry.get(),
                                                    eventdateentry.get(),eventtimeentry.get(),eventvenueentry.get()))
            
            db=sqlite3.connect('userinfo.sqlite')
            cursor = db.cursor()
            cursor.execute("UPDATE schoolevent SET event_name=?,date=?,time=?,venue=? WHERE event_code=?"
                        ,(eventnameentry.get(),eventdateentry.get(),eventtimeentry.get(),eventvenueentry.get(),eventcodeentry.get()))
            db.commit()
            db.close()
            clearentry()
            messagebox.showinfo("Info", "The event details has been sussessfully updated.")
        
        
        
    def delete_data():
        if eventcodeentry.get() == "" or eventnameentry.get() == "" or eventdateentry.get() == "" or eventtimeentry.get() == "" or eventvenueentry.get() == "" :
            messagebox.showerror("Error","Please do not leave any event details blank !")  
        else:
            x=manage_tree.selection()[0]
            manage_tree.delete(x)
            
            db=sqlite3.connect('userinfo.sqlite')
            cursor = db.cursor()
            cursor.execute("DELETE from schoolevent WHERE event_code=?",(eventcodeentry.get(),))
            db.commit()
            db.close()
            clearentry()
            messagebox.showinfo("Info", "The event has been deleted.")
        

    def clearentry():
        eventcodeentry.delete(0, END)
        eventnameentry.delete(0, END)
        eventdateentry.delete(0, END)
        eventtimeentry.delete(0, END)
        eventvenueentry.delete(0, END)


    def select_data(e):
        eventcodeentry.delete(0, END)
        eventnameentry.delete(0, END)
        eventdateentry.delete(0, END)
        eventtimeentry.delete(0, END)
        eventvenueentry.delete(0, END)
        
        select = manage_tree.focus()
        values = manage_tree.item(select, "values")
        
        eventcodeentry.insert(0, values[0])
        eventnameentry.insert(0, values[1])
        eventdateentry.insert(0, values[2])
        eventtimeentry.insert(0, values[3])
        eventvenueentry.insert(0, values[4])


    buttonframe = LabelFrame(manageeventframe, text ="Choose a button to manage")
    buttonframe.place(x=723, y=50)

    deleteevent = Button(buttonframe, text = "Delete Event", command = delete_data)
    deleteevent.grid(row=0, column=0, padx=10, pady=10)

    editevent = Button(buttonframe, text = "Update Event", command=update_data)
    editevent.grid(row=1, column=0, padx=10, pady=10)
    
    Button(manageeventframe,  width=8,pady=5,text="Home",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), 
           command =lambda:raise_frame(adminhomepage)).place(x=820,y=10)

    manage_tree.bind("<ButtonRelease-1>", select_data)
    
    

############################################ view participant ##############################################################

def participant():
    """Set values in the Combobox named cmbo"""
    dbcon = sqlite3.connect('userinfo.sqlite')
    pcur = dbcon.cursor()
    pcur.execute('SELECT event_name FROM schoolevent')
    data = []
    for row in pcur.fetchall():
        data.append(row[0])
    return data

cmbo1 = StringVar()

def check():
    my_w =Tk()
    my_w.geometry("925x500+200+100")
    my_w.configure(bg="#FCE1F3")
    
    conn = sqlite3.connect('userinfo.sqlite')
    c = conn.cursor()
    c=c.execute("""SELECT * FROM student_register_event WHERE event_name=?""",[cmbo.get()])
    i=0 # row value inside the loop 
    for student_register_event in c: 
        for j in range(len(student_register_event )):
            e = Entry(my_w, width=53, fg='blue') 
            e.grid(row=i, column=j)
            e.insert(END, student_register_event[j])
        i=i+1
    my_w.mainloop()

viewparticipantframe = Frame(root, width = 925, height = 500, bg="#FCE1F3")
viewparticipantframe.place(x=0,y=0)
title=Label(viewparticipantframe, text='View Participants', fg="Hotpink2", font=('Time New Roman',26,'bold'), bg='#FCE1F3').place(x=295,y=54)
cmbo = ttk.Combobox(viewparticipantframe, values=participant(),textvariable=cmbo1, width = 60)
cmbo.place(x=235,y=200)
button1 = Button(viewparticipantframe,text="Display data", bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12),command=check).place(x=635,y=195)

################################################# Help Desk ##########################################################################

def send():
	send = "You : " + e.get()
	txt.insert(END, "\n" + send)

	user = e.get().lower()

	if user == "hello":
    
		txt.insert(END, "\n" + "System : Hi, how can I help you?")
  
	elif (user == "hi" or user == "hii" or user == "hiiii"):
		txt.insert(END, "\n" + "System : Hi, how can I help you?")

	elif (user == "how are you"):
		txt.insert(END, "\n" + "System : I'm fine. How about you?")

	elif (user == "I'm fine" or user == "i am good" or user == "i am doing good"):
		txt.insert(END, "\n" + "System : Great! how can I help you.")

	elif (user == "thanks" or user == "thank you" or user == "now its my time"):
		txt.insert(END, "\n" + "System : You are welcome!")

	elif (user == "how to set a event reminder" or user == "how to set event reminder"):
		txt.insert(
			END, "\n" + "System : 1. Click on the reminder. \n 2. Select the time and the date when want to remind you.\n 3.Click on the set reminder button. ")

	elif (user == "goodbye" or user == "bye" or user == "welcome"):
		txt.insert(END, "\n" + "System : Thank you. Have a nice day!")	

	elif (user == "how to register an event" or user == "how to register a event" or user == "how to register event" or 
       user =="how register event" or user == "register event"):
		txt.insert(END, "\n" + "System : 1. Click on the school event. \n 2. Click on the register event. \n 3. Enter your Name, Email, Student ID and Event code.")

	elif (user == "how to check the event i register" or user == "how to check event" or user == "how to check the event" or 
       user =="how to check event" or user == "check event"):
		txt.insert(END, "\n" + "System : 1. Click on the my activities.")

	elif (user == "how do i look for the contact info " or user == "how to check on contact info" or user =="Where can I check for the contact methods "):
		txt.insert(END, "\n" + "System : 1. Click on the more info.")

	else:
        		txt.insert(END, "\n" + "System : Sorry! I didn't understand what you mean.")

helpdeskframe=Frame(root, width = 925, height = 500)
helpdeskframe.place(x=0,y=0)
helpdeskframe=Frame(bg="#FCE1F3")


label1 = Label(helpdeskframe, bg="#FCE1F3", fg="Hotpink2", text="Help Desk", font=("Time New Roman",26,"bold"), pady=6, width=45, height=2).grid(row=0)

txt = Text(helpdeskframe, bg="#FCE1F3", fg="#000000", font=("Time New Roman",13), width=80,height=18)
txt.grid(row=1, column=0, columnspan=5)

    
scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)

e = Entry(helpdeskframe, bg="#FFFFFF", fg="#000000", font=("Time New Roman",20), width=45)
e.grid(row=2, column=0)

send = Button(helpdeskframe, text="Send", width=10,pady=3, font=("Time New Roman",12), bg="#FCE1F3", command=send).place(x=713,y=443)


    
############################################################### School Event ##################################################################

Schoolevent = Frame(root,bg='#FCE1F3',width=925, height=500)
Schoolevent.place(x=0,y=0)

schooleventtitle = Label(Schoolevent, text = "School Events", fg="Hotpink2",bg="#FCE1F3",font=("Time New Roman",26,"bold")).place(x=365,y=54)

f_scroll = Frame(Schoolevent, width=850, height=350)
f_scroll.place(x=30,y=120)
mycanvas = Canvas(f_scroll, bg="white", width=850, height=350)
mycanvas.pack(side=LEFT)
scrollbar=Scrollbar(f_scroll, orient=VERTICAL, command=mycanvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
mycanvas.configure(yscrollcommand=scrollbar.set)
mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion = mycanvas.bbox('all')))

frameincanvas = Frame(mycanvas)
mycanvas.create_window((0,0), window=frameincanvas, anchor="nw")


global i,images
db=sqlite3.connect('userinfo.sqlite')
cursor = db.cursor()
events=cursor.execute("SELECT * FROM schoolevent")

i=0
images = []
for schoolevent in events:
    for r in schoolevent: 
        eventframe = Frame(frameincanvas, bg='antiquewhite1', width=850, height=350)
        eventframe.grid(row=i, column=1, padx=1, pady=3)
        eventname = Label(eventframe, border = 0, text=schoolevent[1]+" "+schoolevent[0], bg='antiquewhite1', font=("Time New Roman", 16))
        eventname.place(x=230,y=20)
        eventdate = Label(eventframe, border = 0, text="Date:"+schoolevent[2], bg='antiquewhite1', font=("Time New Roman", 13))
        eventdate.place(x=230,y=70)
        eventtime = Label(eventframe, border = 0, text="Time:"+schoolevent[3], bg='antiquewhite1', font=("Time New Roman", 13))
        eventtime.place(x=230,y=120)
        eventvenue = Label(eventframe, border = 0, text='Venue:'+schoolevent[4], bg='antiquewhite1', font=("Time New Roman", 13))
        eventvenue.place(x=230, y=170)
        
        image = BytesIO(schoolevent[5])
        image = Image.open(image)
        image = image.resize((190,220))
        image = ImageTk.PhotoImage(image)
        imagelabel = Label(eventframe, image = image)
        imagelabel.place(x=10,y=10)
        images.append(image)
        
        joinbtn = Button(eventframe, width=20,pady=5, text="Register event", bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command= lambda:registerationpage())
        joinbtn.place(x=375, y=300)

          
    i += 1       

################################################################# Schoolevent for admin to view only ##########################################

def schooleventadminview():
    Schooleventforadmin = Frame(root,bg='#FCE1F3',width=925, height=500)
    Schooleventforadmin.place(x=0,y=0)

    Button(Schooleventforadmin,  width=8,pady=5,text="Home",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), 
           command =lambda:raise_frame(adminhomepage)).place(x=830,y=10)  

    schooleventtitle1 = Label(Schooleventforadmin, text = "School Events", fg="Hotpink2",bg="#FCE1F3",font=("Time New Roman",26,"bold")).place(x=365,y=54)

    f_scroll1 = Frame(Schooleventforadmin, width=850, height=350)
    f_scroll1.place(x=30,y=120)
    mycanvas1 = Canvas(f_scroll1, bg="white", width=850, height=350)
    mycanvas1.pack(side=LEFT)
    scrollbar1=Scrollbar(f_scroll1, orient=VERTICAL, command=mycanvas1.yview)
    scrollbar1.pack(side=RIGHT, fill=Y)
    mycanvas1.configure(yscrollcommand=scrollbar1.set)
    mycanvas1.bind('<Configure>', lambda e: mycanvas1.configure(scrollregion = mycanvas1.bbox('all')))

    frameincanvas1 = Frame(mycanvas1)
    mycanvas1.create_window((0,0), window=frameincanvas1, anchor="nw")

    db=sqlite3.connect('userinfo.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM schoolevent")
    events1 = cursor.fetchall()

    global i, images1
    i=0
    images1 = []
    for schoolevents in events1:
        for r in schoolevents: 
            eventframe1 = Frame(frameincanvas1, bg='antiquewhite1', width=850, height=350)
            eventframe1.grid(row=i, column=1, padx=1, pady=3)
            eventname1 = Label(eventframe1, border = 0, text=schoolevents[1]+" "+schoolevents[0], bg='antiquewhite1', font=("Time New Roman", 16))
            eventname1.place(x=230,y=20)
            eventdate1 = Label(eventframe1, border = 0, text="Date:"+schoolevents[2], bg='antiquewhite1', font=("Time New Roman", 13))
            eventdate1.place(x=230,y=70)
            eventtime1 = Label(eventframe1, border = 0, text="Time:"+schoolevents[3], bg='antiquewhite1', font=("Time New Roman", 13))
            eventtime1.place(x=230,y=120)
            eventvenue1 = Label(eventframe1, border = 0, text='Venue:'+schoolevents[4], bg='antiquewhite1', font=("Time New Roman", 13))
            eventvenue1.place(x=230, y=170)
            
            image1 = BytesIO(schoolevents[5])
            image1 = Image.open(image1)
            image1 = image1.resize((190,220))
            image1 = ImageTk.PhotoImage(image1)
            imagelabel1 = Label(eventframe1, image = image1)
            imagelabel1.place(x=10,y=10)
            images1.append(image1)
    
        i += 1 
              
    
############################################################ Student Register For An Event #####################################################################

def registerationpage ():
    root1=Toplevel()
    root1.geometry('400x300+475+260')
    root1.resizable(0,0)
    root1.title('Register event')
    root1.configure(bg ="antiquewhite1")
    
    def vieweventname():
        db = sqlite3.connect('userinfo.sqlite')
        cursor = db.cursor()
        cursor.execute('SELECT event_name FROM schoolevent')
        eventdata = []
        for row in cursor.fetchall():
            eventdata.append(row[0])

        return eventdata
    
    Label(root1, text= "Register",fg="Hotpink2",bg="antiquewhite1",font=("Time New Roman",20,"bold")).place(x=140,y=35)
    Label(root1, text= "Name:",fg="Black",bg="antiquewhite1",font=("Time New Roman",12)).place(x=25,y=110)
    Label(root1, text= "Email:",fg="Black",bg="antiquewhite1",font=("Time New Roman",12)).place(x=25,y=150)
    
    nameentry = Entry(root1, width = 30)
    nameentry.place(x=125,y=110)
    emailentry = Entry(root1, textvariable = emailinput, width = 30)
    emailentry.place(x=125,y=150)
    combobox = ttk.Combobox(root1,width=55, values=vieweventname())
    combobox.place(x=25,y=185)
    combobox.set("Select a school event")
    
    Button(root1, width=12,pady=5, text = "Confirm to join", bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command=lambda :selectEventforRegistration
           (root1,nameentry.get(), emailentry.get(),combobox.get())).place(x=145,y=225)
  

def selectEventforRegistration(root1,name,email,combobox):
    db=sqlite3.connect('userinfo.sqlite')
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS student_register_event(name VARCHAR (30)  NOT NULL, student_email TEXT 
                   REFERENCES user (Email) NOT NULL, event_name VARCHAR (100) REFERENCES schoolevent (event_name) NOT NULL)""")
    cursor.execute("INSERT INTO student_register_event (name, student_email, event_name) VALUES (?,?,?)",(name,email,combobox))
    db.commit()
    db.close()
    root1.destroy()
   
   
# Check my registered events


def myevent():
    
    myeventframe = Frame(root,bg='#FCE1F3',width=925, height=500)
    myeventframe.place(x=0,y=0)
    
    Button(myeventframe, width=8,pady=5,text="Home",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command =lambda:raise_frame(homepage)).place(x=830,y=10)
    myeventtitle = Label(myeventframe, text="My Events", fg="Hotpink2",bg="#FCE1F3",font=("Time New Roman",26,"bold")).place(x=365,y=54)
    
    f_scrollmyevent = Frame(myeventframe, width=600, height=350)
    f_scrollmyevent.place(x=20,y=120)
    mycanvas2 = Canvas(f_scrollmyevent, bg="white", width=600, height=350)
    mycanvas2.pack(side=LEFT)
    scrollbar2=Scrollbar(f_scrollmyevent, orient=VERTICAL, command=mycanvas2.yview)
    scrollbar2.pack(side=RIGHT, fill=Y)
    mycanvas2.configure(yscrollcommand=scrollbar2.set)
    mycanvas2.bind('<Configure>', lambda e: mycanvas2.configure(scrollregion = mycanvas2.bbox('all')))
    frameincanvas2 = Frame(mycanvas2)
    mycanvas2.create_window((0,0), window=frameincanvas2, anchor="nw")
 
    db=sqlite3.connect('userinfo.sqlite')
    cursor = db.cursor()
    allmyevent = cursor.execute("""SELECT name, event_code, event_name, date, time, venue FROM (SELECT sre.name, sre.student_email, 
                                 se.event_code,se.event_name, se.date, se.time, se.venue
                                 FROM student_register_event AS sre JOIN schoolevent AS se
                                 ON sre.event_name=se.event_name) WHERE student_email=?""",(e1.get(),))
    
    count=0
    for registerevent in allmyevent:
            frameinside = Frame(frameincanvas2, bg='antiquewhite1', width=925, height=500)
            frameinside.grid(row=count, column=1, padx=5, pady=3)
            myeventnamenCode = Label(frameinside, text=registerevent[2]+" "+registerevent[1], bg='antiquewhite1', font=("Time New Roman", 18))
            myeventnamenCode.place(x=40,y=25)
            myeventdate = Label(frameinside, text="Date:"+registerevent[3], bg='antiquewhite1', font=("Time New Roman", 13))
            myeventdate.place(x=40,y=70)
            myeventtime = Label(frameinside, text="Time:"+registerevent[4], bg='antiquewhite1', font=("Time New Roman", 13))
            myeventtime.place(x=40,y=110)
            myeventvenue = Label(frameinside, text="Venue:"+registerevent[5], bg='antiquewhite1', font=("Time New Roman", 13))
            myeventvenue.place(x=40, y=150) 
            myname = Label(frameinside, text="Name registered:"+registerevent[0], bg='antiquewhite1', font=("Time New Roman", 13))
            myname.place(x=40,y=190)
            registerstatus = Label(frameinside, text ="RegisterStatus:REGISTERED",bg='antiquewhite1', fg="green", font=("Time New Roman", 13))
            registerstatus.place(x=40,y=230)
            
            Button(frameinside, text="Set Reminder",bg="#F5FFFA",fg="black",border=0, command = lambda:rm()).place(x=455, y=310)
            
            

            count += 1  
    
    labelframeforcalendar = LabelFrame(myeventframe, text="My Calendar")
    labelframeforcalendar.place(x=660, y=120)
    
    cal = Calendar(labelframeforcalendar, selectmode="day", year=2022, month = 12, day = 1)
    cal.grid(pady = 10 )
    
    def grad_date():
        date.config(text="Selected date is:"+cal.get_date())
    
    date = Label(labelframeforcalendar, text="")
    date.grid(pady = 5)
    
    Button(labelframeforcalendar, text = "Get date", command = grad_date).grid(pady=5)
    
    
 ########################################## Reminder ####################################################################################   

    def rm():
        root2 = Toplevel()
        root2.title("My Activity")
        root2.geometry("300x300+500+250")
        root2.configure(bg="#FCE1F3")

        date=StringVar()
        month=StringVar()
        year=StringVar()

        hour=StringVar()
        minute=StringVar()
        second=StringVar()

        def Threading():
            t1=Thread(target=alarm)
            t1.start()
            

        def alarm():
            # Set Alarm
            set_alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
            date2= date.get()
            month2=month.get()
            year2=year.get()
            messagebox.showinfo("Reminder","Reminder Set!!")
            

            while True:
                set_alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                
                today = datetime.datetime.now()
                todays_date = int(today.strftime("%d"))
                todays_month= int(today.strftime("%m"))
                todays_year = int(today.strftime("%Y"))
            
                dt=int(float(date2))
                mth=int(month2)
                yr=int(year2)
            
                set_date = dt - todays_date
                set_month = mth - todays_month
                set_year = yr - todays_year
                
                
                if current_time == set_alarm_time:
                    if set_date == 0 and set_month == 0 and set_year == 0 :
                        messagebox.showinfo("Reminder","Event is coming up")
                

        label1 = Label(root2,text="Reminder",font=("Helvetica 20 bold"),fg="red").place(x=10,y=10)
        label2 = Label(root2,text="Set Time",font=("Helvetica 15 bold")).place(x=10,y=40)
         
        hour = StringVar(root2)
        hours = ('00', '01', '02', '03', '04', '05', '06', '07',
                 '08', '09', '10', '11', '12', '13', '14', '15',
                 '16', '17', '18', '19', '20', '21', '22', '23', '24')
        hour.set(hours[0])
         
        hrs = OptionMenu(root2, hour, *hours)
        hrs.place(x=10,y=70)
        hrs.config(bg='lightpink')
         
        minute = StringVar(root2)
        minutes = ('00', '01', '02', '03', '04', '05', '06', '07',
                   '08', '09', '10', '11', '12', '13', '14', '15',
                   '16', '17', '18', '19', '20', '21', '22', '23',
                   '24', '25', '26', '27', '28', '29', '30', '31',
                   '32', '33', '34', '35', '36', '37', '38', '39',
                   '40', '41', '42', '43', '44', '45', '46', '47',
                   '48', '49', '50', '51', '52', '53', '54', '55',
                   '56', '57', '58', '59', '60')
        minute.set(minutes[0])
         
        mins = OptionMenu(root2, minute, *minutes)
        mins.place(x=65,y=70)
        mins.config(bg='lightblue')

         
        second = StringVar(root)
        seconds = ('00', '01', '02', '03', '04', '05', '06', '07',
                   '08', '09', '10', '11', '12', '13', '14', '15',
                   '16', '17', '18', '19', '20', '21', '22', '23',
                   '24', '25', '26', '27', '28', '29', '30', '31',
                   '32', '33', '34', '35', '36', '37', '38', '39',
                   '40', '41', '42', '43', '44', '45', '46', '47',
                   '48', '49', '50', '51', '52', '53', '54', '55',
                   '56', '57', '58', '59', '60')
        second.set(seconds[0])
         
        secs = OptionMenu(root2, second, *seconds)
        secs.place(x=120,y=70)
        secs.config(bg='lightgreen')

        Label(root2,text="Set Date",font=("Helvetica 15 bold")).place(x=10,y=100)

        date = IntVar(root2)
        dates = ('01', '02', '03', '04', '05', '06', '07',
                   '08', '09', '10', '11', '12', '13', '14', '15',
                   '16', '17', '18', '19', '20', '21', '22', '23',
                   '24', '25', '26', '27', '28', '29', '30','31')
        date.set(dates[0])
         
        dt = OptionMenu(root2, date, *dates)
        dt.place(x=10,y=130)

        month = StringVar(root2)
        months = ('01', '02', '03', '04', '05', '06', '07',
                   '08', '09', '10', '11', '12')
        month.set(months[0])
         
        mth = OptionMenu(root2, month, *months)
        mth.place(x=65,y=130)


        year= StringVar(root2)
        years = ('2022','2023')
        year.set(years[0])
         
        yrs = OptionMenu(root2, year, *years)
        yrs.place(x=120,y=130)

        Button(root2,text="Set Reminder",font=("Helvetica 15"),command=Threading).place(x=10,y=250)

        root2.mainloop()

###################################################################### More Info #####################################################################################
        
def moreinfo():
    moreinfo = Frame(root,bg='#FCE1F3',width=925, height=500)
    moreinfo.place(x=0,y=0)
    Label(moreinfo,text="More Info",fg="Hotpink2",bg="#FCE1F3",font=("Time New Roman",26,"bold")).place(x=365,y=54)
    Label(moreinfo, text="Address",bg="#FCE1F3",justify="left",anchor="nw",font=("Time New Roman",13)).place(x = 290, y = 120)
    Label(moreinfo, text="1-Z Lebuh Bukit Jambul, 11900 Pulau Pinang.",bg="#FCE1F3",justify="left",anchor="nw",font=("Time New Roman",13)).place(x = 290, y = 140)
    Label(moreinfo, text="Office Hour",bg="#FCE1F3",justify="left",anchor="nw",font=("Time New Roman",13)).place(x = 290, y = 190)
    Label(moreinfo, text="Monday to Friday     9a.m. - 6p.m.",bg="#FCE1F3",justify="left",anchor="nw",font=("Time New Roman",13)).place(x = 290, y = 210)
    Label(moreinfo, text="Contact Number",bg="#FCE1F3",justify="left",anchor="nw",font=("Time New Roman",13)).place(x = 290, y = 260)
    Label(moreinfo, text="Telephone no.     (+604) 631 0138",bg="#FCE1F3",justify="left",anchor="nw",font=("Time New Roman",13)).place(x = 290, y = 280)
    Label(moreinfo, text="Fax no.               (+604) 631 0138",bg="#FCE1F3",justify="left",anchor="nw",font=("Time New Roman",13)).place(x = 290, y = 300)
    Label(moreinfo, text="Website",bg="#FCE1F3",justify="left",anchor="nw",font=("Time New Roman",13)).place(x = 290, y = 350)
    Label(moreinfo, text="www.newinti.edu.my",bg="#FCE1F3",justify="left",anchor="nw",font=("Time New Roman",13)).place(x = 290, y = 370)
    Label(moreinfo, text="Email",bg="#FCE1F3",justify="left",anchor="nw",font=("Time New Roman",13)).place(x = 290, y = 420)
    Label(moreinfo, text="_iicp.adco@newinti.edu.my",bg="#FCE1F3",justify="left",anchor="nw",font=("Time New Roman",13)).place(x = 290, y = 440)

    Button(moreinfo, width=8,pady=5,text="Home",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command =lambda:raise_frame(homepage)).place(x=830,y=10)
  
######################################################################## Homepage #####################################################################################

homepage=Frame(root,width=925,height=500,bg="#FCE1F3")
homepage.place(x=0,y=0)

heading=Label(homepage,text="School Announcement System",fg="Hotpink2",bg="#FCE1F3",font=("Time New Roman",26,"bold"))
heading.place(x=225,y=54)

btn2=Button(homepage,width=30,pady=5,text="School Event",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command=lambda:raise_frame(Schoolevent)).place(x=130,y=170)
btn3=Button(homepage,width=30,pady=5,text="Help Desk",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command=lambda:raise_frame(helpdeskframe)).place(x=130,y=320)
btn4=Button(homepage,width=30,pady=5,text="More Info",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command=lambda:moreinfo()).place(x=520,y=320)
btn5=Button(homepage, width=30,pady=5,text="My Activity",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command=lambda:myevent()).place(x=520,y=170)
btn1=Button(homepage, width=10,pady=5,text="Log Out",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command=lambda:raise_frame(l)).place(x=413,y=440)

####################################################### admin homepage ##################################################################

adminhomepage=Frame(root,width=925,height=500,bg="#FCE1F3")
adminhomepage.place(x=0,y=0)

heading=Label(adminhomepage,text="School Announcement System",fg="Hotpink2",bg="#FCE1F3",font=("Time New Roman",26,"bold"))
heading.place(x=225,y=54)

btn1=Button(adminhomepage,width=30,pady=5,text="Add Event",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command=lambda:raise_frame(add_eventframe)).place(x=130,y=170)
btn2=Button(adminhomepage,width=30,pady=5,text="Manage Event",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command = lambda:manageeventadmin()).place(x=130,y=320)
btn3=Button(adminhomepage,width=30,pady=5,text="View Participant",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command = lambda:raise_frame(viewparticipantframe)).place(x=520,y=320)
btn4=Button(adminhomepage,width=30,pady=5,text="School Events",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command = lambda:schooleventadminview()).place(x=520,y=170)
btn5=Button(adminhomepage, width=10,pady=5,text="Log Out",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command=lambda:raise_frame(l)).place(x=413,y=440)

#################################################### Register and login ####################################################################3   
def database():
    global db, cursor
    db=sqlite3.connect('userinfo.sqlite')
    cursor = db.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS user(Name TEXT, Email TEXT, password TEXT)")


def Login():
    database()
    if e1.get() == '' or e2.get() == '' :
        messagebox.showerror('Error', 'Please complete the required field !')
    elif e1.get() == "Admin12345" and e2.get() == "Admin12345" :
        messagebox.showinfo("Info", "Welcome Back Admin")
        adminhomepage.tkraise()
    else:       
        cursor.execute("SELECT * FROM user WHERE Email = ? and Password = ?", (e1.get(), e2.get()))
        if cursor.fetchone() is not None :
           messagebox.showinfo('Info', 'Login Successfully')
           homepage.tkraise()
        else:
           messagebox.showerror('Error', 'Invalid email or password')
           db.commit()   
        
def Register():
    database()
    if registername.get() == '' or registeremail.get() == '' or registerpassword.get() == '' or confirmpassword.get() == '':
        messagebox.showerror('Error', 'Please complete the required field !')
    elif registerpassword.get() != confirmpassword.get() :
        messagebox.showerror('Error', 'Password does not match !')    
    elif len(registerpassword.get()) < 4 or len(confirmpassword.get()) < 4 :
        messagebox.showerror('Error', 'Password must beat least 5 characters !')
    else:
        test = cursor.execute("SELECT Email FROM user WHERE Email=?",(registeremail.get(),))
        if cursor.fetchone() is not None:
            messagebox.showerror('Error', 'Account has been registered!')    
        else:
            cursor.execute("INSERT INTO user(Name, Email, Password) VALUES(?,?,?)", (registername.get(), registeremail.get(), registerpassword.get()))
            if TRUE :
               messagebox.showinfo('Info', 'Register Successfully')
               l.tkraise()
               db.commit() 
               db.close()
        
     
        
#loginpage
l=Frame(root,width=925,height=500,bg='#FCE1F3')
l.place(x=0,y=0)

# Entry for gmail 
logibtitle=Label(l, text='Log In',fg="Hotpink2", font=('Time New Roman',26,'bold'), bg='#FCE1F3').place(x=420,y=54)
l1=Label(l, text="Email:", font=('Time New Roman',12), bg='lightpink')
l1.place(x=200,y=150)
e1=Entry(l,width=60,fg='black', font=('Time New Roman',12), textvariable=emailinput)
e1.place(x=200,y=175)
                
# Entry for password 
l2=Label(l, text="Password:", font=('Time New Roman',12), bg='lightpink')
l2.place(x=200,y=240)
e2=Entry(l,width=60,fg='black', font=('Time New Roman',12),show="*")
e2.place(x=200,y=265)
       
loginbtn=Button(l,font=('Time New Roman',12),text='             Login             ',border=2,bg='#F5FFFA',fg='black', command=Login )
loginbtn.place(x=300,y=360)

 

#registerpage
w=Frame(root,width=925,height=500,bg='#FCE1F3')
w.place(x=0,y=0)

# Entry for name
Registertitle=Label(w, text='Register',fg="Hotpink2", font=('Time New Roman',26,'bold'), bg='#FCE1F3').place(x=395,y=54)
l3=Label(w, text="Name:", font=('Time New Roman',12), bg='lightpink')
l3.place(x=200,y=120)
registername=Entry(w,width=60,fg='black', font=('Time New Roman',12))
registername.place(x=200,y=145)
               
# Entry for email 
l4=Label(w, text="Email:", font=('Time New Roman',12), bg='lightpink')
l4.place(x=200,y=185)
registeremail=Entry(w,width=60,fg='black', font=('Time New Roman',12))
registeremail.place(x=200,y=210)
    
# Entry for password
l5=Label(w, text="Password:", font=('Time New Roman',12), bg='lightpink')
l5.place(x=200,y=250)
registerpassword=Entry(w,width=60,fg='black', font=('Time New Roman',12),show="*")
registerpassword.place(x=200,y=275)

l6=Label(w, text="Confirm Password:", font=('Time New Roman',12), bg='lightpink')
l6.place(x=200,y=315)
confirmpassword=Entry(w,width=60,fg='black', font=('Time New Roman',12),show="*")
confirmpassword.place(x=200,y=340)

registerbtn=Button(w,font=('Time New Roman',12),text='        Register        ',border=2,bg='#F5FFFA',fg='black', command=Register)
registerbtn.place(x=310,y=400)

for frame in (Schoolevent, Reminder, helpdeskframe, adminhomepage, viewparticipantframe, add_eventframe):
    frame.grid(row=0, column=0, sticky='news')    
    
    
Button(l, text = 'Create new account', font=('Time New Roman',12), border=2,bg='#F5FFFA',fg='black', command=lambda:raise_frame(w)).place(x=500,y=360)   
Button(w, text = 'Back to Login Page', font=('Time New Roman',12), border=2,bg='#F5FFFA',fg='black', command=lambda:raise_frame(l)).place(x=500,y=400)
Button(Schoolevent, width=8,pady=5,text="Home",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command=lambda:raise_frame(homepage)).place(x=830,y=10)
Button(helpdeskframe, width=8,pady=5,text="Home",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command =lambda:raise_frame(homepage)).place(x=830,y=10)
Button(viewparticipantframe, width=8,pady=5,text="Home",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command =lambda:raise_frame(adminhomepage)).place(x=830,y=10)
Button(add_eventframe,  width=8,pady=5,text="Home",bg="#F5FFFA",fg="black",border=0,font=("Time New Roman",12), command =lambda:raise_frame(adminhomepage)).place(x=830,y=10)


root.mainloop()
