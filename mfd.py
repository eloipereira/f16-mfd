from state_machine import *
from tkinter import Frame, Tk, Label, BOTH
from select import select
from evdev import InputDevice, categorize, ecodes
from PIL import Image, ImageTk
import configparser as cp
import imageio
import re

# Config
config = cp.ConfigParser()
config.read('config.ini')

dev = InputDevice(config['DEFAULT']['MFD_DEVICE'])
filename = config['DEFAULT']['STF_FILE']
img_folder = config['DEFAULT']['IMAGES_FOLDER']
img_extension = config['DEFAULT']['FIG_EXT']
video_extension = config['DEFAULT']['VID_EXT']

class MFD_App(Frame):
    def __init__(self, state_transition = None, master=Tk(), img_folder = img_folder):
        Frame.__init__(self,master)
        self.state_transition = state_transition
        self.master = master
        self.init_window()
        self.img_path = img_folder + "/{0!s}" 

    def init_window(self):
        self.master.geometry("800x600")
        self.master.wm_attributes('-type','splash')
        self.master.attributes('-fullscreen',True)
        self.pack(fill=BOTH, expand=1)
        
    def show_menu(self):
        if re.match("(\S+)."+img_extension , self.state_transition.state.name): 
            img = ImageTk.PhotoImage(Image.open(self.img_path.format(self.state_transition.state)))
            self.panel = Label(self, image=img)
            self.panel.configure(background='black')
            self.panel.image = img
            self.panel.pack(fill = "both", expand = "yes")
            self.update_idletasks()
            self.update()
        elif re.match("(\S+)."+video_extension , self.state_transition.state.name):
            print("First menu cannot be a video.")
        else:
            print("Unknown extension.")

    def update_menu(self):
        if re.match("(\S+)."+img_extension , self.state_transition.state.name): 
            img2 = ImageTk.PhotoImage(Image.open(self.img_path.format(self.state_transition.state)))
            self.panel.configure(background='black')
            self.panel.configure(image=img2)
            self.panel.image = img2
            self.update_idletasks()
        elif re.match("(\S+)."+video_extension , self.state_transition.state.name):
            video = imageio.get_reader(self.img_path.format(self.state_transition.state))
            for frame in video.iter_data():
                frame_img = ImageTk.PhotoImage(Image.fromarray(frame))
                self.panel.configure(background='black')
                self.panel.configure(image=frame_img)
                self.panel.image = frame_img
                self.update_idletasks()
        else:
            print("Unknown extension.")
                
    def events_loop(self):
        r, w, x = select([dev], [],[])
        for e in r[0].read():
            if e.type == ecodes.EV_KEY and e.value == 1:
                if self.state_transition.state_update(e.code,from_code = True):
                    self.update_menu()
        self.after(100,self.events_loop())

st = StateTransition(from_file = True, filename = filename)
app = MFD_App(st)
app.show_menu()
app.events_loop()
