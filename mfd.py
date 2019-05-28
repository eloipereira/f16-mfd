from state_machine import *
from tkinter import Frame, Tk, Label, BOTH
from select import select
from evdev import InputDevice, categorize, ecodes
from PIL import Image, ImageTk
import configparser as cp

# Config
config = cp.ConfigParser()
config.read('config.ini')

dev = InputDevice(config['DEFAULT']['MFD_DEVICE'])
filename = config['DEFAULT']['STF_FILE']
img_folder = config['DEFAULT']['IMAGES_FOLDER']
img_extension = config['DEFAULT']['FIG_EXT']

class MFD_Window(Frame):
    def __init__(self, state_transition = None, master=Tk(), img_folder = img_folder, img_extension = img_extension):
        Frame.__init__(self,master)
        self.state_transition = state_transition
        self.master = master
        self.init_window()
        self.img_path = img_folder + "/{0!s}." + img_extension

    def init_window(self):
        self.master.geometry("800x600")
        self.master.wm_attributes('-type','splash')
        self.pack(fill=BOTH, expand=1)
        
    def show_menu(self):
        img = ImageTk.PhotoImage(Image.open(self.img_path.format(self.state_transition.state)))
        self.panel = Label(self, image=img)
        self.panel.image = img
        self.panel.pack(fill = "both", expand = "yes")
        self.update_idletasks()
        self.update()

    def update_menu(self):
        img2 = ImageTk.PhotoImage(Image.open(self.img_path.format(self.state_transition.state)))
        self.panel.configure(image=img2)
        self.panel.image = img2
        self.update_idletasks()
        self.update()

    def events_loop(self):
        r, w, x = select([dev], [],[])
        for e in r[0].read():
            if e.type == ecodes.EV_KEY and e.value == 1:
                if self.state_transition.state_update(e.code,from_code = True):
                    self.update_menu()
        self.after(100,self.events_loop())


st = StateTransition(from_file = True, filename = filename)
app = MFD_Window(st)
app.show_menu()
app.events_loop()
