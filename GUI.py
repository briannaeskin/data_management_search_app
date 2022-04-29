# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 20:36:38 2022

@author: Michael Gleyzer
"""



#Import the required Libraries  
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
#Create an instance of Tkinter frame
win = Tk()
#Set the geometry of Tkinter frame
win.geometry("750x270")

entry = StringVar()
def submit():
    global entry
    print(entry.get())
    return entry.get()

def open_popup_tweet():
   top= Toplevel(win)
   top.geometry("750x250")
   top.title("Tweet")
   e = Entry(top, textvariable = entry)
   e.pack()
   ttk.Button(top,text = "Submit",command = submit).pack()
   
   
def open_popup_user(): 
   top= Toplevel(win)
   top.geometry("750x250")
   top.title("User search")
   e = Entry(top, textvariable = entry)
   e.pack()
   ttk.Button(top,text = "Submit",command = submit).pack()
   
def open_popup_timerange(): 
   top= Toplevel(win)
   top.geometry("750x250")
   top.title("time range")
   searched_h = StringVar()  
   e = Entry(top , textvariable = entry)
   e.pack() 
   ttk.Button(top,text = "Submit",command = submit).pack()
   
def open_popup_hashtag():
   top= Toplevel(win)
   top.geometry("750x250")
   top.title("hashtag search")
   e = Entry(top , textvariable = entry)
   e.pack() 
   ttk.Button(top,text = "Submit",command = submit).pack()
             
#   Label(top, text= "Hello World!", font=('Mistral 18 bold')).place(x=150,y= 80)
   
Label(win, text="What do you want to search for?", font=('Helvetica 14 bold')).pack(pady=20)
#Create a button in the main Window to open the popup
ttk.Button(win, text= "User", command= open_popup_user).pack()
ttk.Button(win , text = "Tweet" , command=open_popup_tweet ).pack()
ttk.Button(win, text = "Hashtag" , command=open_popup_hashtag).pack() 
ttk.Button(win, text = "Time Range" , command = open_popup_timerange).pack()
win.mainloop()

if __name__ == "main" : 
    submit()