import json
import customtkinter as ctk
from time import sleep
import os
import sys
from Layout import CurrentConditionsPanel, UIPanel, SevenDayPanel, HourlyPanel
from Logic import AppLogic

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
        ctk.set_appearance_mode("dark") #light mode doesn't really work with current visuals
        
        #variables
        self.program_run = True 
        self.base_font = ("Arial", 15)
        self.current_font = ("Arial", 16)
        self.mid_font = ("Arial", 13)
        self.hourly_font = ("Arial", 12)

        #asset sub-directories
        self.data_path = "Assets\\Data"
        self.icon_path = "Assets\\Icons"

        self.set_user_files_path()
        
        #attempt to fill city vars on run, if fails to load from json display message in UI Panel
        try:
            with open(self.user_files_path + "\\user_options.json", "r") as user_data_import: 
                json_import = json.load(user_data_import)
            self.selected_city_var = ctk.StringVar(value=(json_import.get("City Name") + ", " + json_import.get("Region Name") + ", " + json_import.get("Country"))) #country name to be added here
            self.selected_lat = json_import.get("Latitude")
            self.selected_long = json_import.get("Longitude")
            #self.selected_city_loaded = True #variable not in use: could be used to pause api reqs if no city selected
        except FileNotFoundError:
            self.selected_city_var = ctk.StringVar(value="No City Selected. Open Options Menu to Select a City")
            self.selected_lat = ""
            self.selected_long = ""
            #self.selected_city_loaded = False

        #WIDGETS
        #logic
        self.app_logic = AppLogic(self)

        #Frame Structure for Main Page
        self.ui_panel = UIPanel(self, self.base_font, self.app_logic)
        self.current_conditions_frame = CurrentConditionsPanel(self, self.current_font, self.app_logic)
        self.seven_day_frame = SevenDayPanel(self, self.base_font, self.mid_font,self.app_logic)
        self.hourly_frame = HourlyPanel(self, self.hourly_font, self.app_logic)
              
        #LAYOUT
        #Main panels
        self.ui_panel.grid(row=0, column=0, columnspan=2, sticky="new")
        self.current_conditions_frame.grid(row=1, column=0, sticky="news")
        self.seven_day_frame.grid(row=1, column=1, sticky="news", padx=1)
        self.hourly_frame.grid(row=2, column=0, columnspan=2, sticky="news")

        self.bind("<Configure>", self.on_move_window)
        self.protocol("WM_DELETE_WINDOW", self.terminate_api_reqs)
        #allow applogic to alter panel widgets and data
        self.app_logic.give_applogic_panel_access(self.current_conditions_frame, self.seven_day_frame, self.hourly_frame)

        #icon file needs .exe or .py directory
        try:
            exe_path = os.getcwd()
        except Exception:
            exe_path = os.path.dirname(os.path.abspath(sys.executable))
        icon_path = os.path.join(exe_path, "Icon.ico")
        self.iconbitmap(icon_path)

        self.mainloop()
    
    #set up file directories
    #User Generated Files
    def set_user_files_path(self):
        self.user_path = os.path.expanduser("~") #ref to User folder in Windows
        self.user_files_path = os.path.join(self.user_path, "Documents\\Era Desktop Weather")
        try:
            os.mkdir(self.user_files_path)
        except FileExistsError:
            pass
        except FileNotFoundError:
            print("Documents folder not found: launch process for user to select alternative.")

    #Program Assets (except .ico)
    def get_prog_assets_path(self, asset_path):
        try:
            self.main_path = sys._MEIPASS # type: ignore (sys._MEIPASS is not an attribute of sys, its a temp folder) 
        except Exception:
            self.main_path = os.getcwd()
        return os.path.join(self.main_path, asset_path)

    #end api requests when main window is closed
    def terminate_api_reqs(self):
        self.program_run = False
        #wait until current api req is done processing, then close window which ends api thread(s)
        self.app_logic.event.wait()
        self.destroy()
        
    def on_move_window(self, event):
        if event.widget == self:
            sleep(0.015)

main_window = MainWindow("Era Desktop Weather", (960, 540))
