# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 20:36:38 2022

@author: Michael Gleyzer
"""



#Import the required Libraries  
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import json
import search_app
from datetime import datetime

#Create an instance of Tkinter frame
win = Tk()
#Set the geometry of Tkinter frame
win.geometry("750x270")

entry = StringVar()
time_entry = StringVar()

#User presses submit button and function returns the user's inputs 
def submit_user():
    global entry
    global time_entry

    top = Toplevel(win)
    top.geometry("750x250")
    top.title("User Search Results")

    input = entry.get()

    if time_entry.get() == "":
        timerange_lower = None
        timerange_upper = None

    else:
        timerange_lower, timerange_upper = time_entry.get().strip().split(',')
        timerange_lower = datetime.strptime(timerange_lower.strip(), '%m/%d/%Y %H:%M:%S') if timerange_lower else None
        timerange_upper = datetime.strptime(timerange_upper.strip(), '%m/%d/%Y %H:%M:%S') if timerange_upper else None

    search_query = search_app.Search()


    result = search_query.search_by_user(input, timerange_lower, timerange_upper)
    #if time_entry.get() == "" :
    #    return entry.get() , ""
    #time_range = json.loads(time_entry.get())
    #return entry.get() , time_range

    output_label = Label(top, text=result, wraplength=1500)
    output_label.pack()

def submit_tweet():
    global entry
    global time_entry

    top = Toplevel(win)
    top.geometry("750x250")
    top.title("Tweet Text Search Results")

    input = entry.get()

    if time_entry.get() == "":
        timerange_lower = None
        timerange_upper = None

    else:
        timerange_lower, timerange_upper = time_entry.get().strip().split(',')
        timerange_lower = datetime.strptime(timerange_lower.strip(), '%m/%d/%Y %H:%M:%S') if timerange_lower else None
        timerange_upper = datetime.strptime(timerange_upper.strip(), '%m/%d/%Y %H:%M:%S') if timerange_upper else None

    search_query = search_app.Search()


    result = search_query.search_by_text(input, timerange_lower, timerange_upper)
    #if time_entry.get() == "" :
    #    return entry.get() , ""
    #time_range = json.loads(time_entry.get())
    #return entry.get() , time_range

    output_label = Label(top, text=result, wraplength=1500)
    output_label.pack()

def submit_hashtag():
    global entry
    global time_entry

    top = Toplevel(win)
    top.geometry("750x250")
    top.title("Hashtag Search Results")

    input = entry.get()

    if time_entry.get() == "":
        timerange_lower = None
        timerange_upper = None

    else:
        timerange_lower, timerange_upper = time_entry.get().strip().split(',')
        timerange_lower = datetime.strptime(timerange_lower.strip(), '%m/%d/%Y %H:%M:%S') if timerange_lower else None
        timerange_upper = datetime.strptime(timerange_upper.strip(), '%m/%d/%Y %H:%M:%S') if timerange_upper else None

    search_query = search_app.Search()


    result = search_query.search_by_hashtag(input, timerange_lower, timerange_upper)
    #if time_entry.get() == "" :
    #    return entry.get() , ""
    #time_range = json.loads(time_entry.get())
    #return entry.get() , time_range

    output_label = Label(top, text=result, wraplength=1500)
    output_label.pack()



# User selects option to input a tweet and query time range
def open_popup_tweet():
   top= Toplevel(win)
   top.geometry("750x250")
   top.title("Tweet")
   
   Label(top, text="Input Tweet", font=('Helvetica 14 bold')).pack(pady=20)
   e = Entry(top, textvariable = entry)
   e.pack()
   
   Label(top, text="What time range do you want? (Format of input: [start,end])", font=('Helvetica 14 bold')).pack(pady=20)
   t = Entry(top , textvariable = time_entry)
   t.pack()
   
   ttk.Button(top,text = "Submit",command = submit_tweet).pack()
   
# User selects option to input a user and query time range   
def open_popup_user(): 
   top= Toplevel(win)
   top.geometry("750x250")
   top.title("User search")
   
   Label(top, text="Input User", font=('Helvetica 14 bold')).pack(pady=20)
   e = Entry(top, textvariable = entry)
   e.pack()
   
   Label(top, text="What time range do you want? (Format of input: [start,end], with start/end of format mm/dd/yyyy H:M:S)", font=('Helvetica 14 bold')).pack(pady=20)
   t = Entry(top , textvariable = time_entry)
   t.pack()
   ttk.Button(top,text = "Submit",command = submit_user).pack()

#User selects option to input a hashtag and query time range
def open_popup_hashtag():
   top= Toplevel(win)
   top.geometry("750x250")
   top.title("hashtag search")
   
   Label(top, text="Input Hashtag", font=('Helvetica 14 bold')).pack(pady=20)
   e = Entry(top , textvariable = entry)
   e.pack() 
   
   Label(top, text="What time range do you want? (Format of input: [start,end])", font=('Helvetica 14 bold')).pack(pady=20)
   t = Entry(top , textvariable = time_entry)
   t.pack()
   
   ttk.Button(top,text = "Submit",command = submit_hashtag).pack()
   
Label(win, text="What do you want to search for?", font=('Helvetica 14 bold')).pack(pady=20)

#Create a button in the main Window to open the popup
ttk.Button(win, text= "User", command= open_popup_user).pack()
ttk.Button(win , text = "Tweet" , command=open_popup_tweet).pack()
ttk.Button(win, text = "Hashtag" , command=open_popup_hashtag).pack()
win.mainloop()
