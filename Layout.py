import customtkinter as ctk
from PIL import Image
import requests
import json
import datetime
from itertools import islice, chain
from Options_Menu import OptionsMenu
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

        #variables
        today = datetime.datetime.now().weekday()
        hour = datetime.datetime.now().hour
        self.current_font = ("Arial", 16)
        self.base_font = ("Arial", 15)
        self.hourly_font = ("Arial", 12)
        self.placeholder_image = ctk.CTkImage(light_image=Image.open("test image.png"))
        self.selected_city_var = ctk.StringVar(value="No City Selected")
        self.selected_lat = "default"
        self.selected_long = "default"

        #instantiate frame classes
        self.app_logic = AppLogic(self)

        self.current_conditions_frame = CurrentConditionsPanel(self, self.current_font, self.app_logic, self.placeholder_image)
        self.ui_panel = UIPanel(self, self.base_font, self.placeholder_image)
        self.seven_day_frame = SevenDayPanel(self, self.base_font, self.app_logic, self.placeholder_image, today)
        self.hourly_frame = HourlyPanel(self, self.hourly_font, self.app_logic, self.placeholder_image, hour)
        
        #layout
        self.ui_panel.grid(row=0, column=0, columnspan=2, sticky="new")
        self.current_conditions_frame.grid(row=1, column=0, sticky="news")
        self.seven_day_frame.grid(row=1, column=1, sticky="news")
        self.hourly_frame.grid(row=2, column=0, columnspan=2, sticky="news")

        self.mainloop()

class CurrentConditionsPanel(ctk.CTkFrame):
    def __init__(self, parent, font, app_logic, placeholder_image): 
        super().__init__(master=parent)

        self.parent = parent

        #panel chars
        self.configure(fg_color="#008575", border_color="#000000", border_width=1, corner_radius=0)
        
        #widgets
        self.current_cond_title = ctk.CTkLabel(self, bg_color="#008575", text="Current Conditions", font=font, height=20)
        self.current_cond_temp = ctk.CTkLabel(self, bg_color="#008575", text="", font=font, compound="left", image=placeholder_image, corner_radius=0, height=20)
        self.current_cond_desc = ctk.CTkLabel(self, bg_color="#008575", text="", font=font, height=20)
        self.current_cond_humidity = ctk.CTkLabel(self, bg_color="#008575", text="", font=font, height=20)
        self.current_cond_feels = ctk.CTkLabel(self, bg_color="#008575", text="", font=font, height=20)
        self.current_cond_wind = ctk.CTkLabel(self, bg_color="#008575", text="", font=font, height=20)
        self.current_cond_gust = ctk.CTkLabel(self, bg_color="#008575", text="", font=font, corner_radius=0, height=20)
        self.current_cond_mm = ctk.CTkLabel(self, bg_color="#008575", text="", font=font, corner_radius=0, height=20)
        self.current_cond_pressure = ctk.CTkLabel(self, bg_color="#008575", text="", font=font, corner_radius=0, height=20)

        #layout
        self.current_cond_title.pack(pady=(12,10))
        self.current_cond_temp.pack()
        self.current_cond_desc.pack(pady=(10,0))
        self.current_cond_humidity.pack(pady=(10,0))
        self.current_cond_feels.pack()
        self.current_cond_wind.pack(pady=(8,0))
        self.current_cond_gust.pack(pady=(0,8))
        self.current_cond_mm.pack()
        self.current_cond_pressure.pack(pady=(4,0))

        #start recursive api call and widget config for current conditions
        app_logic.get_current_cond_thread(app_logic.get_current_cond)

class UIPanel(ctk.CTkFrame):
    def __init__(self, parent, font, placeholder_image):
        super().__init__(master=parent)

        #panel chars
        self.configure(fg_color="#003030", corner_radius=0)

        #parent
        self.parent = parent
        
        #widgets
        self.selected_city_display = ctk.CTkLabel(self, textvariable=self.parent.selected_city_var, font=font, bg_color="#003030", text_color="#999999", wraplength=940, anchor="w")
        self.refresh_data = ctk.CTkButton(self, text="", image=placeholder_image, font=font, fg_color="#005050", corner_radius=0, width=10, command=lambda: self.refresh())
        self.options = ctk.CTkButton(self, text="", image=placeholder_image, font=font, fg_color="#005050", corner_radius=0, width=10, command=lambda: self.open_options_menu(parent, font))

        #layout
        self.options.pack(side="left", pady=1)
        self.refresh_data.pack(side="left", pady=1)
        self.selected_city_display.pack(side="left", fill="x", pady=1, padx=3)

    def open_options_menu(self, parent, font):
        parent.app_logic.load_city_data()
        self.options_menu = OptionsMenu(parent, font, parent.app_logic, parent.app_logic.city_list, self.parent.selected_city_var, self.parent.selected_lat, self.parent.selected_long)
        self.options_menu.grid(row=0, rowspan=3, column=0, columnspan=2, sticky="news")
        self.options_menu.tkraise()
    
    def refresh(self):
        print("This is a refresh button, it will eventually send all 3 api requests and update displayed data")
        print(self.parent.selected_city_var.get())
        print(self.parent.selected_lat, self.parent.selected_long)

class SevenDayPanel(ctk.CTkFrame):
    def __init__(self, parent, font, app_logic, placeholder_image, today):
        super().__init__(master=parent)
        self.grid_columnconfigure((0,1,2,3,4,5,6), weight=1, uniform="a")
        self.grid_rowconfigure(0, weight=1)

        #panel chars
        self.configure(fg_color="#005050", border_color="#000000", border_width=1, corner_radius=0)

        #subframes
        self.seven_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.days_of_wk = self.resort_days(self.seven_days, today)
        day_frame_list = []
        for i, day in enumerate(self.days_of_wk):
            #frames
            self.day_frame = ctk.CTkFrame(self, width=109, fg_color="#008575", border_color="#000000", border_width=1, corner_radius=0)
            #widgets NOTE also remove placeholder text and images here in final version
            day_frame_title = ctk.CTkLabel(self.day_frame, text=day, font=font)
            day_frame_icon = ctk.CTkLabel(self.day_frame, text="", image=placeholder_image, height=15)
            day_frame_high = ctk.CTkLabel(self.day_frame, text="High: 25 C\nFeels: 28 C", font=font, height=30)
            day_frame_low = ctk.CTkLabel(self.day_frame, text="Low: 14 C\nFeels: 16 C", font=font, height=30)
            day_frame_humid = ctk.CTkLabel(self.day_frame, text="Humidity: 60 %", font=font, height=15)
            day_frame_wind = ctk.CTkLabel(self.day_frame, text="Wind: 25 Kph\nGust: 40 Kph", font=font, height=30)
            day_frame_precip = ctk.CTkLabel(self.day_frame, text="POP: 75 %\n4 mm", font=font, height=30)

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

    def resort_days(self, list, today):
        iterable = iter(list)
        next(islice(iterable, today, today), None)
        return chain(iterable, islice(list, today))

class HourlyPanel(ctk.CTkScrollableFrame):
    def __init__(self, parent, font, app_logic, placeholder_image, hour):
        super().__init__(master=parent)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1, uniform="a")
        self.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1, uniform="a")

        #panel chars
        self.configure(fg_color="#005050", corner_radius=0, border_color="#000000", border_width=1)

        #generate subframes and hours
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
            self.hour_frame = ctk.CTkFrame(self, fg_color="#008575", height=133, width=77, border_width=1, border_color="#000000", corner_radius=0)
            #widgets NOTE also remove placeholder text and images from here in final version
            self.hour_title = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text=hour_str, font=font, corner_radius=0, height=18)
            self.hour_temp = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="35 C", compound="left", image=placeholder_image, font=font, corner_radius=0, height=15)
            self.hour_feels = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="Feels: 38 C", font=font, corner_radius=0, height=15)
            self.hour_wind = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="Wind: 25 Kph", font=font, corner_radius=0, height=15)
            self.hour_gust = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="Gust: 30 Kph", font=font, corner_radius=0, height=15)
            self.hour_precip = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="POP: 30%", font=font, corner_radius=0, height=15)
            self.hour_mm = ctk.CTkLabel(self.hour_frame, bg_color="#008575", text="10mm", font=font, corner_radius=0, height=15)
            #layout
            self.hour_frame.grid(row=row_count, column=column_count, sticky="nwse", padx=1, pady=1)
            self.hour_title.pack(pady=(2,1))
            self.hour_temp.pack()
            self.hour_feels.pack(pady=1)
            self.hour_wind.pack(pady=(2,0))
            self.hour_gust.pack(pady=(0,2))
            self.hour_precip.pack(pady=(2,0))
            self.hour_mm.pack(pady=(0,2))
            column_count += 1
            hour += 1
            hour_total += 1

            self.hour_frame_list.append(self.hour_frame)

if __name__ == "__main__":
    main_window = MainWindow("Testing Layout", (960, 540))