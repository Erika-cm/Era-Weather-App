import xml.etree.ElementTree as et
import requests
import xml
import json
import pandas as pd
import customtkinter as ctk
from PIL import Image
from tkinter import ttk
from itertools import islice, chain
import datetime
from time import sleep
#from searchable_list_ui import SearchableDropdownMenu
from Options_Menu import OptionsMenu
from Layout import CurrentConditionsPanel, UIPanel, SevenDayPanel, HourlyPanel

class MainWindow(ctk.CTk):
    def __init__(self, title, windowsize):
        super().__init__()

        #window stuff
        self.title(title)
        self.geometry(f'{windowsize[0]}x{windowsize[1]}')
        self.grid_rowconfigure(0, weight=1, uniform="a")
        self.grid_rowconfigure((1,2), weight=10, uniform="a") #can pass a list(range(2) to spec number of cols/rows in place of (0,1) in this case)
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=4, uniform="a")
        
        #variables
        today = datetime.datetime.now().weekday()
        hour = datetime.datetime.now().hour
        self.base_font = ("Arial", 15)
        self.current_font = ("Arial", 16)
        self.hourly_font = ("Arial", 12)
        self.placeholder_image = ctk.CTkImage(light_image=Image.open("test image.png"))
        self.selected_city_var = ctk.StringVar(value="No City Selected")

        #WIDGETS
        #Frame Structure for Main Page
        self.current_conditions_frame = CurrentConditionsPanel(self, self.current_font, self.placeholder_image)
        self.ui_panel = UIPanel(self, self.base_font, self.placeholder_image, self.selected_city_var)
        self.seven_day_frame = SevenDayPanel(self, self.base_font, self.placeholder_image, today)
        self.hourly_frame = HourlyPanel(self, self.hourly_font, self.placeholder_image, hour)
              
        #LAYOUT
        #Main panels
        self.ui_panel.grid(row=0, column=0, sticky="new")
        self.current_conditions_frame.grid(row=1, column=0, sticky="news")
        self.seven_day_frame.grid(row=0, rowspan=2, column=1, sticky="news", padx=1)
        self.hourly_frame.grid(row=2, column=0, columnspan=2, sticky="news")

        self.bind("<Configure>", self.on_move_window)
        
        self.mainloop()

        #icon file needs .exe or .py directory
        # try:
        #     exe_path = os.getcwd()
        # except Exception:
        #     exe_path = os.path.dirname(os.path.abspath(sys.executable))
        # icon_path = os.path.join(exe_path, "Icon.ico")
        # self.iconbitmap(icon_path)

    def on_move_window(self, event):
        if event.widget == self:
            sleep(0.015)
       
main_window = MainWindow("Title", (960, 540))
