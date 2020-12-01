#! /usr/bin/env/python3
from tkinter import *

number = ""

def press(nume):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(nume))

def num_get():
    global number
    num = number.get()
    print(num)
    num=""
    number.set(num)

root = Tk()
root.title("Input Number")


number = StringVar()

entry = Frame(root)
entry.grid(row=5, column=3, sticky='news')

Label(entry, text="Enter the Phone Number").grid(columnspan=3, row=0, column=0)
e = Entry(entry, textvariable=number)
e.grid(columnspan=3, row=1, column=0)
Button(entry, text='1', bg='green', fg='white', command=lambda:press(1)).grid(row=2, column=0)
Button(entry, text='2', bg='green', fg='white', command=lambda:press(2)).grid(row=2, column=1)
Button(entry, text='3', bg='green', fg='white', command=lambda:press(3)).grid(row=2, column=2)
Button(entry, text='4', bg='green', fg='white', command=lambda:press(4)).grid(row=3, column=0)
Button(entry, text='5', bg='green', fg='white', command=lambda:press(5)).grid(row=3, column=1)
Button(entry, text='6', bg='green', fg='white', command=lambda:press(6)).grid(row=3, column=2)
Button(entry, text='7', bg='green', fg='white', command=lambda:press(7)).grid(row=4, column=0)
Button(entry, text='8', bg='green', fg='white', command=lambda:press(8)).grid(row=4, column=1)
Button(entry, text='9', bg='green', fg='white', command=lambda:press(9)).grid(row=4, column=2)
Button(entry, text='0', bg='green', fg='white', command=lambda:press(0)).grid(row=5, column=0)
Button(entry, text='Enter', bg='green', fg='white', command=num_get).grid(columnspan=2, row=5, column=1)

root.mainloop()
