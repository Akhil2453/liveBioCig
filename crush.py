#! /usr/bin/env python3
import RPi.GPIO as GPIO
import time
from tkinter import *
import tkinter.font as tkFont
import requests
from PIL import Image, ImageTk

def raise_frame(frame):
    frame.tkraise()

#Declare Global Variables
root = None
dfont = None
welcome = None
msg = None
value = None
number = ""

#GPIO pins
aux_vcc = 16
s2 = 5
s3 = 6
signal = 26
NUM_CYCLES = 10
visible = None

#Fulscreen or windowed
fullscreen = False

def count10():
    t=10
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer,"\r")
        time.sleep(1)
        t -= 1

def number_e():
    global number
    global visible
    num = number.get()
    number.set(num)
    print(num)
    para = {'action': 'saveUserData', 'MOB': num, 'MCID': '002000501', 'BTNO': '10'}
    r = requests.post("http://clickcash.in/apisave/apiDataSavever2.php", data=para)
    print(r.text)
    visible = True
    num=""
    number.set(num)
    raise_frame(PageTwo)
    root.after(10000, PageTwo.lower)
    raise_frame(welcome)

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
    raise_frame(welcome)

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
    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.LOW)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start      #seconds to run for loop
    red  = NUM_CYCLES / duration   #in Hz
    #print("red value - ",red)
    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration
    #print("blue value - ",blue)
    GPIO.output(s2,GPIO.HIGH)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    green = NUM_CYCLES / duration
    #print("green value - ",green)
    time.sleep(0.5)
    #if ((red >= 4000 and red <= 5000) and (blue >= 4000 and blue <= 5000) and (green >= 4000 and green <= 5500)):
    #    print("Place the Cigarette")
    #    msge="Place the\nCigarette"
    #    msg.set(msge)
        #raise_frame(welcome)
    #if ((red >= 3600 and red <= 4299) and (blue >= 3900 and blue <= 5850) and (green >= 5150 and green <= 6300)):
    #    print("Cigarette Bud Detected 1")
    #    msge="Cigarette bud\nDetectedd"
    #    msg.set(msge)
    #    raise_frame(PageOne)
    #elif ((red >= 3600 and red <= 4999) and (blue >= 4199 and blue <= 4800) and (green >= 4500 and green <= 5950)):
    #    print("Cigarette Bud Detected 2")
    #    msge="Cigarette bud\nDetectedd"
    #    msg.set(msge)
    #    raise_frame(PageOne)
    #elif ((red >= 4400 and red <= 4699) and (blue >= 4150 and blue <= 5000) and (green >= 4100 and green <= 4950)):
    #    print("Cigarette Bud Detected 3")
    #    msge="Cigarette bud\nDetectedd"
    #    msg.set(msge)
    #    raise_frame(PageOne)
    #elif ((red >= 5000 and red <= 5600) and (blue >= 5000 and blue <= 5600) and (green >= 3900 and green <= 4499)):
    #    print("Cigarette Bud Detected 4")
    #    msge="Cigarette bud\nDetectedd"
    #    msg.set(msge)
    #    raise_frame(PageOne)
    #else:
    #    print("Place the Cigarette")
    #    msge="Place the\nCigarette"
    #    msg.set(msge)
    if (((red >= 4150 or red >= 4000 or red >= 3000 or (red >= 2200 and red <= 3000) or (red >= 0 and red <= 170) or (red > 3801)) and red <= 5099)): #and ((blue >= 5150 or blue >= 4300 or (blue >= 2700 and blue <= 2799)) and blue <= 5699) and  ((green >= 4000 or green >= 3200 or (green >= 2200 and green <= 3100)) and green <= 4650)):
        print("Place the Cigarette")
        print("red value: ", red)
        msge="Place the\nCigarette"
        msg.set(msge)
    #elif((red >= 4800 and red <= 4899) and (blue >= 4500 and blue <= 5300)):
    elif((red >= 3500 and red <= 3600) and (blue >= 3000 and blue <= 4900)):
        print("Cigarette Bud Detected Orange")
        msge="Cigarette bud\nDetectedd"
        msg.set(msge)
        raise_frame(PageOne)
    else:
        print("red value: ", red)
        print("blue value: ", blue)
        print("green value: ", green)
        print("Cigarette Bud Detected all")
        msge="Cigarette bud\nDetectedd"
        msg.set(msge)
        raise_frame(PageOne)
    root.after(500, loop)

#create the window
root = Tk()
root.title("Cigarette Bud Crusher: BioCrux")
root.geometry('800x480')

welcome = Frame(root)
PageOne = Frame(root)
PageTwo = Frame(root)

for frame in (welcome, PageOne, PageTwo):
    frame.grid(row=6, column=3, sticky='news')

value = DoubleVar()
msg = StringVar()
number = StringVar()

dfont = tkFont.Font(size=-6)
myfont = tkFont.Font(size=20)
mfont = tkFont.Font(size=12)
wel = Label(welcome, text="Welcome.\nPlease extinguish and drop your Cigarette bud here", font=myfont)
wel.grid(row=1, column=1, padx=0, pady=0)
wel.place(x=50, y=320)
load = Image.open("banner.png")
load = load.resize((800,250), Image.BICUBIC)
render = ImageTk.PhotoImage(load)
img = Label(welcome, image=render)
img.image = render
img.place(x=0, y=0)
img.grid(row=0, column=0)

Label(PageOne, text="Enter your Mobile Number to get reward: ", font=myfont).grid(columnspan=3, row=0, column=0, padx=100, pady=50)
e = Entry(PageOne, textvariable=number, width=30, font=myfont)
e.grid(columnspan=3, row=1, column=0, padx=150, pady=15)
Button(PageOne, text='1', command=lambda:num_get(1), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=2, column=0)
Button(PageOne, text='2', command=lambda:num_get(2), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=2, column=1)
Button(PageOne, text='3', command=lambda:num_get(3), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=2, column=2)
Button(PageOne, text='4', command=lambda:num_get(4), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=3, column=0)
Button(PageOne, text='5', command=lambda:num_get(5), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=3, column=1)
Button(PageOne, text='6', command=lambda:num_get(6), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=3, column=2)
Button(PageOne, text='7', command=lambda:num_get(7), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=4, column=0)
Button(PageOne, text='8', command=lambda:num_get(8), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=4, column=1)
Button(PageOne, text='9', command=lambda:num_get(9), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=4, column=2)
Button(PageOne, text='0', command=lambda:num_get(0), borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=5, column=1)
Button(PageOne, text='Delete', command=delt, borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=5, column=2)
Button(PageOne, text='Clear', command=clr, borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=5, column=0)
Button(PageOne, text='Enter', bg='#0052cc', fg='#ffffff', command=number_e, borderwidth=5, relief=RAISED, height=1, width=20, font=myfont).grid(row=6, column=0, columnspan=2)
Button(PageOne, text='Cancel', command=cancel, borderwidth=5, relief=RAISED, height=1, width=10, font=myfont).grid(row=6, column=2)

Label(PageTwo, text=" ", font=myfont).grid(row=0, column=1, padx=5, pady=5)
Label(PageTwo, text="Thank You", font=myfont).grid(row=1, column=1, padx=150, pady=200)
Button(PageTwo, text="welcomeScreen", command=lambda:raise_frame(welcome)).grid(row=2, column=1, padx=35, pady=35)


root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

root.bind('<Configure>', resize)

setup()

root.after(1000, loop)
raise_frame(welcome)
toggle_fullscreen()
root.mainloop()
