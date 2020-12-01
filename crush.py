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
    para = {'action': 'saveUserData', 'MOB': num, 'MCID': '002000244', 'BTNO': '10'}
    r = requests.post("http://clickcash.in/apisave/apiDataSavever2.php", data=para)
    print(r.text)
    visible = True
    num=" "
    number.set(num)
    raise_frame(PageTwo)
    root.after(10000, PageTwo.lower)
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
    GPIO.output(s2, GPIO.HIGH)
    GPIO.output(s3, GPIO.LOW)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    val = NUM_CYCLES / duration
    value.set(val)
    print("value: ", val)
    if val > 5600:
        print("Cigarette Bud Detected")
        msge="Cigarette bud\nDetectedd"
        msg.set(msge)
        raise_frame(PageOne)
    else:
        print("Place the Cigarette")
        msge="Place the\nCigarette"
        msg.set(msge)
    root.after(500, loop)

#create the window
root = Tk()
root.title("Cigarette Bud Crusher: BioCrux")
root.geometry('800x480')

welcome = Frame(root)
PageOne = Frame(root)
PageTwo = Frame(root)

for frame in (welcome, PageOne, PageTwo):
    frame.grid(row=5, column=3, sticky='news')

value = DoubleVar()
msg = StringVar()
number = StringVar()

dfont = tkFont.Font(size=-12)

#space=Label(welcome, text="                ", font=dfont)
#space.grid(row=0, column=0, padx=40, pady=40)
Label(welcome, text="Welcome.\n Please extinguish and drop your Cigarette bud here", font=dfont).grid(row=0, column=0, padx=50, pady=75)

#Label(PageOne, text=" ", font=dfont).grid(row=0, column=1, padx=5, pady=5)
Label(PageOne, text="Enter your Mobile Number to get reward: ", font=dfont).grid(row=1, column=1, padx=25, pady=15)
Entry(PageOne, textvariable=number, width=30, font=dfont).grid(row=2, column=1, padx=25, pady=13)
Button(PageOne, text='Enter', font=dfont, command=number_e).grid(row=3, column=1, padx=50, pady=25)

Label(PageTwo, text=" ", font=dfont).grid(row=0, column=1, padx=5, pady=5)
Label(PageTwo, text="Thank You", font=dfont).grid(row=1, column=1, padx=150, pady=50)
Button(PageTwo, text="welcomeScreen", command=lambda:raise_frame(welcome)).grid(row=2, column=1, padx=35, pady=35)

#for frame in (welcome, PageOne, PageTwo):
#    frame.rowconfigure(1, weight=1)
#for frame in (welcome, PageOne, PageTwo):
#    frame.columnconfigure(1, weight=1)

root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

root.bind('<Configure>', resize)

setup()

root.after(1000, loop)
raise_frame(welcome)
#toggle_fullscreen()
root.mainloop()
