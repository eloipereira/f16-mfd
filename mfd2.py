from tkinter import Frame, Tk, Label, BOTH
from select import select
from evdev import InputDevice, categorize, ecodes
from PIL import Image, ImageTk
import re


class State:
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()
    def __eq__(self,other):
        return self.name == other.name
    def __ne__(self,other):
        return self.name != other.name
    def __hash__(self):
        return hash(self.name)
    
class Event:
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()
    def __eq__(self,other):
        return self.name == other.name
    def __ne__(self,other):
        return self.name != other.name
    def __hash__(self):
        return hash(self.name)

code_to_event = {
        714: Event('GAIN_UP'),
        715: Event('GAIN_DOWN'),
        304: Event('B1'),
        305: Event('B2'),
        306: Event('B3'),
        307: Event('B4'),
        308: Event('B5'),
        708: Event('SYM_UP'),
        709: Event('SYM_DOWN'),
        309: Event('B6'),
        310: Event('B7'),
        311: Event('B8'),
        312: Event('B9'),
        313: Event('B10'),
        710: Event('CON_UP'),
        711: Event('CON_DOWN'),
        314: Event('B11'),
        315: Event('B12'),
        316: Event('B13'),
        317: Event('B14'),
        318: Event('B15'),
        712: Event('BRT_UP'),
        713: Event('BRT_DOWN'),
        319: Event('B16'),
        704: Event('B17'),
        705: Event('B18'),
        706: Event('B19'),
        707: Event('B20')
    }


filename = "state_update_func.txt"
state_transition = {}
regex = "\((\S+)\,(\S+)\)->(\S+)"

with open(filename) as fh:
    for line in fh:
        line = line.replace(' ','')
        t = re.findall(regex,line)[0]
        state_transition[(State(t[0]),Event(t[1]))] = State(t[2])

print(state_transition)



class Window(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("F-16 MFD")
        self.pack(fill=BOTH, expand=1)
        
    def show_img(self, path):
        load = Image.open(path)
        render = ImageTk.PhotoImage(load)
        self.img = Label(self, image=render)
        self.img.image = render
        self.img.place(x=0,y=0)
        self.img.pack()

           
root = Tk()
root.geometry("800x600")
root.wm_attributes('-type','splash')

app = Window(root)
app.show_img(path="images/MAIN_GRID.png")

state = State('MAIN')

dev = InputDevice('/dev/input/event15')
print(dev)

def events_loop(state):
    r, w, x = select([dev], [],[])
    for e in r[0].read():
        if e.type == ecodes.EV_KEY and e.value == 1:
            event = code_to_event[e.code]
            print("Current state: {0!s}".format(state))
            print("Event: {0!s}".format(event))
            try:
                state = state_transition[(state,event)]
                print("New state: {0!s}".format(state))
            except:
                print("Unknown transition")
    root.update_idletasks()
    root.update()
    root.after(100,events_loop(state))

    
events_loop(state)


