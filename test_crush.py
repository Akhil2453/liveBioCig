#! /usr/bin/env python3
import RPi.GPIO as GPIO
import time
from tkinter import *
import tkinter.font as tkFont
import requests

def raise_frame(frame):
    frame.tkraise()

#Declare Global Variables
root = None
dfont = None
welcome = None
msg = None
value = None
number = ""
count = ""
cnt = 0
a = 0

#GPIO pins
aux_vcc = 16
s2 = 5
s3 = 6
signal = 26
NUM_CYCLES = 10

#Fulscreen or windowed
fullscreen = False

def number_e():
    global number
    global visible
    global count
    global cnt
    num = number.get()
    number.set(num)
    print(num)
    cnt = cnt + 1
    count.set(cnt)
    print("count: ", cnt)
    raise_frame(countScreen)

def next():
    global number
    global visible
    global count
    global cnt
    global a
    global num
    raise_frame(PageTwo)
    root.update()
    pushCnt = str(cnt)
    print("Number in next: ")
    print(number)
    print(pushCnt)
    para = {'action': 'saveUserData', 'MOB': num, 'MCID': '002000501', 'BTNO': pushCnt}
    r = requests.post("http://clickcash.in/apisave/apiDataSavever2.php", data=para)
    print(r.text)
    visible = True
    num=""
    number.set(num)
    cnt = 0
    count.set(num)
    a = 0
    time.sleep(5)
    raise_frame(welcome)
    root.update()

def num_get(num):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(num))

def delt():
    temp = e.get()[:-1]
    e.delete(0, END)
    e.insert(0, temp)

def clr():
    e.delete(0, END)

def cancel():
    global cnt
    raise_frame(welcome)
    cnt = 0

#toggle fullscreen
def toggle_fullscreen(event=None):
    global root
    global fullscreen
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize()

#go into windowed mode
def end_fullscreen(event=None):
    global root
    global fullscreen
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize()

#resize font based on screen size
def resize(event=None):
    global dfont
    global welcome
    new_size = -max(12, int((welcome.winfo_height() / 10)))
    dfont.configure(size=new_size)

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(signal, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(aux_vcc, GPIO.OUT)
    GPIO.output(aux_vcc, GPIO.HIGH)
    GPIO.setup(s2, GPIO.OUT)
    GPIO.setup(s3, GPIO.OUT)
    print("\n")

def endprogram():
    GPIO.cleanup()

def loop():
    temp = 1
    global root
    global value
    global msg
    global number
    global num
    global visible
    global count
    global cnt
    a = int(input("enter 1 or 0: "))
    if ((a == 1) and (cnt == 0)):
        msge="Cigarette bud\nDetectedd"
        msg.set(msge)
        raise_frame(PageOne)
        #time.sleep(3)
    else:
        cnt = cnt + 1
        count.set(cnt)
        print("count: ", cnt)
        raise_frame(countScreen)
    root.after(500, loop)

#create the window
root = Tk()
root.title("Cigarette Butt Crusher: BioCrux")
root.geometry('800x480')

welcome = Frame(root)
PageOne = Frame(root)
PageTwo = Frame(root)
countScreen = Frame(root)

for frame in (welcome, PageOne, PageTwo, countScreen):
    frame.grid(row=7, column=3, sticky='news')

value = DoubleVar()
msg = StringVar()
number = StringVar()
count = StringVar()

dfont = tkFont.Font(size=-6)
myfont = tkFont.Font(size=20)
mfont = tkFont.Font(size=12)
tyFont = tkFont.Font(size=40)
wel = Label(welcome, text="Welcome\nPlease extinguish and drop your Cigarette butt here", font=myfont)
wel.grid(row=0, column=1, padx=0, pady=0)
wel.place(x=50, y=185)

cS = Label(countScreen, text="Cigarette Count: ", font=myfont)
cS.place(x=250, y=200)
cS1 = Label(countScreen, textvariable=count, font=myfont)
cS1.place(x=500, y=200)
cSbt = Button(countScreen, text="Next", height=2, width=15, command=lambda:next())
cSbt.place(x=315, y=275)

Label(PageOne, text="Enter your Mobile Number: ", font=myfont).grid(columnspan=3, row=0, column=0, padx=100, pady=20)
e = Entry(PageOne, textvariable=number, width=30, font=myfont)
e.grid(columnspan=3, row=2, column=0, padx=150, pady=25)
Button(PageOne, text='1', command=lambda:num_get(1), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=3, column=0)
Button(PageOne, text='2', command=lambda:num_get(2), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=3, column=1)
Button(PageOne, text='3', command=lambda:num_get(3), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=3, column=2)
Button(PageOne, text='4', command=lambda:num_get(4), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=4, column=0)
Button(PageOne, text='5', command=lambda:num_get(5), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=4, column=1)
Button(PageOne, text='6', command=lambda:num_get(6), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=4, column=2)
Button(PageOne, text='7', command=lambda:num_get(7), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=5, column=0)
Button(PageOne, text='8', command=lambda:num_get(8), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=5, column=1)
Button(PageOne, text='9', command=lambda:num_get(9), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=5, column=2)
Button(PageOne, text='0', command=lambda:num_get(0), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=6, column=1)
Button(PageOne, text='Delete', command=delt, borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=6, column=2)
Button(PageOne, text='Clear', command=clr, borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=6, column=0)
Button(PageOne, text='Enter', bg='#0052cc', fg='#ffffff', command=number_e, borderwidth=5, relief=RAISED, height=1, width=27, font=myfont).grid(row=7, column=0, columnspan=2)
Button(PageOne, text='Cancel', command=cancel, borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=7, column=2)

Label(PageTwo, text="Thank You", font=tyFont).place(x=325, y=200)

root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

root.bind('<Configure>', resize)

setup()

root.after(1000, loop)
raise_frame(welcome)
toggle_fullscreen()
root.mainloop()
