from state_machine import *
from tkinter import Frame, Tk, Label, BOTH
from select import select
from evdev import InputDevice, categorize, ecodes
from PIL import Image, ImageTk
import re

# Config

initial_state = State('MAIN')
dev = InputDevice('/dev/input/event15')
filename = "state_update_func.txt"

state_transition = {}
regex = "\((\S+)\,(\S+)\)->(\S+)"

with open(filename) as fh:
    for line in fh:
        line = line.replace(' ','')
        t = re.findall(regex,line)[0]
        state_transition[(State(t[0]),Event(t[1]))] = State(t[2])

class Window(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.geometry("800x600")
        self.master.wm_attributes('-type','splash')
        self.pack(fill=BOTH, expand=1)
        
    def show_img(self, path):
        img = ImageTk.PhotoImage(Image.open(path))
        self.panel = Label(self, image=img)
        self.panel.image = img
        self.panel.pack(fill = "both", expand = "yes")
        self.update_idletasks()
        self.update()

    def update_img(self,path):
        img2 = ImageTk.PhotoImage(Image.open(path))
        self.panel.configure(image=img2)
        self.panel.image = img2
        self.update_idletasks()
        self.update()
            
app = Window(Tk())
app.show_img(path="images/{0!s}.png".format(initial_state))

def events_loop(state,app):
    r, w, x = select([dev], [],[])
    for e in r[0].read():
        if e.type == ecodes.EV_KEY and e.value == 1:
            event = code_to_event[e.code]
            print("Current state: {0!s}".format(state))
            print("Event: {0!s}".format(event))
            try:
                state = state_transition[(state,event)]
                print("New state: {0!s}".format(state))
                app.update_img(path="images/{0!s}.png".format(state))
            except:
                print("Unknown transition")
    app.after(100,events_loop(state,app))
    
events_loop(initial_state,app)
