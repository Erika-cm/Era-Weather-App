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

class MainWindow(ctk.CTk):
    def __init__(self, title, windowsize):
        super().__init__()

        #window stuff
        self.title(title)
        self.geometry(f'{windowsize[0]}x{windowsize[1]}')
        self.grid_rowconfigure((0,1), weight=1, uniform="a") #can pass a list(range(2) to spec number of cols/rows in place of (0,1) in this case)
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=4, uniform="a")
        
        #variables
        today = datetime.datetime.now().weekday()
        hour = datetime.datetime.now().hour
        self.base_font = ("Arial", 15)
        self.hourly_font = ("Arial", 12)
        self.placeholder_image = ctk.CTkImage(light_image=Image.open("test image.png"))
        self.selected_city_var = ctk.StringVar(value="No City Selected")

        #WIDGETS
        #Frame Structure for Main Page
        self.current_cond_frame = ctk.CTkFrame(self, fg_color="#005050", border_color="#000000", border_width=1, corner_radius=0)
        self.current_cond_frame.grid_columnconfigure((0,1), weight=1, uniform="a")
        self.current_cond_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1, uniform="a")
        self.seven_day_frame = ctk.CTkFrame(self, fg_color="#005050", border_color="#000000", border_width=1, corner_radius=0)
        self.seven_day_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1, uniform="a")
        self.seven_day_frame.grid_rowconfigure(0, weight=1)
        self.hourly_frame = ctk.CTkScrollableFrame(self, fg_color="#005050", corner_radius=0, border_color="#000000", border_width=1)
        self.hourly_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1, uniform="a")
        self.hourly_frame.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1, uniform="a")

        #subframe for current cond (options, refresh, city display)
        self.ui_panel = ctk.CTkFrame(self.current_cond_frame, fg_color="#003030", corner_radius=0)

        #UI Panel
        self.selected_city_display = ctk.CTkLabel(self.ui_panel, textvariable=self.selected_city_var, bg_color="#003030", text_color="#999999")
        self.refresh_data = ctk.CTkButton(self.ui_panel, text="", image=self.placeholder_image, fg_color="#005050", corner_radius=0, width=10, command=self.test_data_storage)
        self.options = ctk.CTkButton(self.ui_panel, text="", image=self.placeholder_image, fg_color="#005050", corner_radius=0, width=10, command=self.open_options_menu)

        #Current Conditions NOTE remove placeholder text and images in final version
        self.current_cond_title = ctk.CTkLabel(self.current_cond_frame, bg_color="#008575", text="Current Conditions", font=self.base_font)
        self.current_cond_temp = ctk.CTkLabel(self.current_cond_frame, bg_color="#008575", text="25 C", font=self.base_font, compound="left", image=self.placeholder_image, corner_radius=0)
        self.current_cond_desc = ctk.CTkLabel(self.current_cond_frame, bg_color="#008575", text="Freezing Drizzle: light", font=self.base_font)
        self.current_cond_humidity = ctk.CTkLabel(self.current_cond_frame, bg_color="#008575", text="Humidity: 60%", font=self.base_font)
        self.current_cond_feels = ctk.CTkLabel(self.current_cond_frame, bg_color="#008575", text="Feels Like: 29 C", font=self.base_font)
        self.current_cond_wind = ctk.CTkLabel(self.current_cond_frame, bg_color="#008575", text="Wind: 25 Kph", font=self.base_font)
        self.current_cond_gust = ctk.CTkLabel(self.current_cond_frame, bg_color="#008575", text="Gust: 35 Kph", font=self.base_font, corner_radius=0)
        self.current_cond_pop = ctk.CTkLabel(self.current_cond_frame, bg_color="#008575", text="POP: 65%", font=self.base_font, corner_radius=0)
        self.current_cond_mm = ctk.CTkLabel(self.current_cond_frame, bg_color="#008575", text="10 mm", font=self.base_font, corner_radius=0)

        #LAYOUT
        #frames
        self.current_cond_frame.grid(row=0, column=0, sticky="nsew")
        self.ui_panel.grid(row=0, column=0, columnspan=2, sticky="new")
        self.seven_day_frame.grid(row=0, column=1, sticky="nsew", padx=1)
        self.hourly_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        #UI panel
        self.options.pack(side="left", pady=1)
        self.refresh_data.pack(side="left", pady=1)
        self.selected_city_display.pack(side="left", fill="x", pady=1, padx=3)

        #Current Conditions
        self.current_cond_title.grid(row=1, column=0, columnspan=2, sticky="sew")
        self.current_cond_temp.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.current_cond_desc.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.current_cond_humidity.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.current_cond_feels.grid(row=5, column=0, columnspan=2, sticky="nsew")
        self.current_cond_wind.grid(row=6, column=0, columnspan=2, sticky="nsew")
        self.current_cond_gust.grid(row=7, column=0, columnspan=2, sticky="new")
        self.current_cond_pop.grid(row=8, column=0, columnspan=2, sticky="nsew")
        self.current_cond_mm.grid(row=9, column=0, columnspan=2, sticky="nsew")

        #7-14 Day Forecast
        #subframes
        self.seven_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.days_of_wk = self.resort_days(self.seven_days, today)
        day_frame_list = []
        for i, day in enumerate(self.days_of_wk):
            #frames
            self.day_frame = ctk.CTkFrame(self.seven_day_frame, width=109, fg_color="#008575", border_color="#000000", border_width=1, corner_radius=0)
            #widgets NOTE also remove placeholder text and images here in final version
            day_frame_title = ctk.CTkLabel(self.day_frame, text=day, font=self.base_font)
            day_frame_icon = ctk.CTkLabel(self.day_frame, text="", image=self.placeholder_image, height=15)
            day_frame_high = ctk.CTkLabel(self.day_frame, text="High: 25 C\nFeels: 28 C", font=self.base_font, height=30)
            day_frame_low = ctk.CTkLabel(self.day_frame, text="Low: 14 C\nFeels: 16 C", font=self.base_font, height=30)
            day_frame_humid = ctk.CTkLabel(self.day_frame, text="Humidity: 60 %", font=self.base_font, height=15)
            day_frame_wind = ctk.CTkLabel(self.day_frame, text="Wind: 25 Kph\nGust: 40 Kph", font=self.base_font, height=30)
            day_frame_precip = ctk.CTkLabel(self.day_frame, text="POP: 75 %\n4 mm", font=self.base_font, height=30)

            #layout
            self.day_frame.grid(row=0, column=i, sticky="nsew", padx=1)
            day_frame_title.pack(pady=1)
            day_frame_icon.pack(pady=1)
            day_frame_high.pack(pady=5)
            day_frame_low.pack(pady=5)
            day_frame_humid.pack(pady=5)
            day_frame_wind.pack(pady=5)
            day_frame_precip.pack(pady=(5,0))

            day_frame_list.append(self.day_frame)
        
        #hourly (72 hours) forecast
        hour_total = 0
        row_count = 0
        column_count=0
        self.hour_frame_list = []
        hour_str = ""
        while hour_total < 72:
            if hour > 24: #reset hour to 1
                hour = 1
            if column_count >= 12:
                column_count = 0 #reset col
                row_count += 1 #adv row
            if hour > 12:
                hour_str = str((hour - 12)) + " PM" #convert to 12 hr clock
            elif hour <= 12:
                hour_str = str(hour) + " AM" #simply convert to string, append AM
            
            #frames
            self.hour_frame = ctk.CTkFrame(self.hourly_frame, fg_color="#008575", height=133, width=77, border_width=1, border_color="#000000", corner_radius=0)
            #widgets NOTE also remove placeholder text and images from here in final version
            self.hour_title = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text=hour_str, font=self.hourly_font, corner_radius=0, height=18)
            self.hour_temp = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="35 C", compound="left", image=self.placeholder_image, font=self.hourly_font, corner_radius=0, height=15)
            self.hour_feels = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="Feels: 38 C", font=self.hourly_font, corner_radius=0, height=15)
            self.hour_wind = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="Wind: 25 Kph", font=self.hourly_font, corner_radius=0, height=15)
            self.hour_gust = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="Gust: 30 Kph", font=self.hourly_font, corner_radius=0, height=15)
            self.hour_precip = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="POP: 30%", font=self.hourly_font, corner_radius=0, height=15)
            self.hour_mm = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="10mm", font=self.hourly_font, corner_radius=0, height=15)
            #layout
            self.hour_frame.grid(row=row_count, column=column_count, sticky="nwse", padx=1, pady=1)
            self.hour_title.pack(pady=(5,2))
            self.hour_temp.pack()
            self.hour_feels.pack(pady=1)
            self.hour_wind.pack(pady=(3,0))
            self.hour_gust.pack(pady=(0,3))
            self.hour_precip.pack(pady=(3,0))
            self.hour_mm.pack(pady=(0,2))
            column_count += 1
            hour += 1
            hour_total += 1
            self.hour_frame_list.append(self.hour_frame)

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

    def open_options_menu(self):
        self.options_menu = OptionsMenu(self, self.selected_city_var)
        self.options_menu.grid(row=0, rowspan=2, column=0, columnspan=2, sticky="nsew")
        self.options_menu.tkraise()
    
    def test_data_storage(self):
        print(self.options_menu.selected_lat)
        print(self.options_menu.selected_long)
        print(self.options_menu.selected_city_var.get())
        test_req = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.options_menu.selected_lat}&longitude={self.options_menu.selected_long}&current=temperature_2m&forecast_days=1&timezone=auto")
        print(test_req.status_code)
        print(test_req.json())

    def resort_days(self,list, today):
            iterable = iter(list)
            next(islice(iterable, today, today), None)
            return chain(iterable, islice(list, today))
        
       
main_window = MainWindow("Title", (960, 540))
