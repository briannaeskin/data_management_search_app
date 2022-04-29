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

#Create an instance of Tkinter frame
win = Tk()
#Set the geometry of Tkinter frame
win.geometry("750x270")

entry = StringVar()
time_entry = StringVar()

#User presses submit button and function returns the user's inputs 
def submit():
    global entry
    global time_entry
    if time_entry.get() == "" : 
        return entry.get() , ""
    time_range = json.loads(time_entry.get())
    return entry.get() , time_range

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
   
   ttk.Button(top,text = "Submit",command = submit).pack()
   
# User selects option to input a user and query time range   
def open_popup_user(): 
   top= Toplevel(win)
   top.geometry("750x250")
   top.title("User search")
   
   Label(top, text="Input User", font=('Helvetica 14 bold')).pack(pady=20)
   e = Entry(top, textvariable = entry)
   e.pack()
   
   Label(top, text="What time range do you want? (Format of input: [start,end])", font=('Helvetica 14 bold')).pack(pady=20)
   t = Entry(top , textvariable = time_entry)
   t.pack()
   ttk.Button(top,text = "Submit",command = submit).pack()

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
   
   ttk.Button(top,text = "Submit",command = submit).pack()
             
   
Label(win, text="What do you want to search for?", font=('Helvetica 14 bold')).pack(pady=20)

#Create a button in the main Window to open the popup
ttk.Button(win, text= "User", command= open_popup_user).pack()
ttk.Button(win , text = "Tweet" , command=open_popup_tweet ).pack()
ttk.Button(win, text = "Hashtag" , command=open_popup_hashtag).pack() 
win.mainloop()
